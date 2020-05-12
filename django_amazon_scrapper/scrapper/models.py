from uuid import uuid4

from django.db.models import (
    CASCADE, BooleanField, CharField, DateField, DateTimeField, FloatField,
    ForeignKey, IntegerField, Model, PositiveSmallIntegerField, TextField,
    UUIDField)

from django_amazon_scrapper.scrapper.choices import (
    AmazonRegion, ProductStatus, ScrapeStatus)
from django_amazon_scrapper.scrapper.utils import (
    AMAZON_PREFIX, PARSER_MAP, TLD_MAP)


class BaseModel(Model):
    created_at = DateTimeField(auto_now_add=True, editable=False)
    updated_at = DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.id


class Asin(BaseModel):
    id = CharField(max_length=20, primary_key=True)
    is_active = BooleanField(default=True)

    def __str__(self):
        return self.id


class Product(BaseModel):
    asin = ForeignKey(Asin, related_name='products', on_delete=CASCADE)
    id = UUIDField(default=uuid4, primary_key=True, editable=False)
    price = FloatField(default=0.0)
    question_count = IntegerField(default=0)
    rating = FloatField(default=0.0)
    region = PositiveSmallIntegerField(choices=AmazonRegion.CHOICES, default=AmazonRegion.US)  # noqa: E501
    review_count = IntegerField(default=0)
    status = PositiveSmallIntegerField(choices=ProductStatus.CHOICES, default=ProductStatus.NEWLY_ADDED)  # noqa: E501
    title = CharField(max_length=5000)

    @property
    def prefix(self):
        tld = TLD_MAP[self.region]
        return f'{AMAZON_PREFIX}.{tld}'

    @property
    def parser(self):
        return PARSER_MAP[self.region]

    def product_url(self):
        return f'{self.prefix}/dp/{self.asin_id}'

    def reviews_url(self, page_number=1):
        return f'{self.prefix}/product-reviews/{self.asin_id}?pageNumber={page_number}&sortBy=recent'  # noqa: E501

    def questions_url(self, page_number=1):
        return f'{self.prefix}/ask/questions/asin/{self.asin_id}/{page_number}?sort=SUBMIT_DATE'  # noqa: E501

    def answers_url(self, question_id, page_number=1):
        return f'{self.prefix}/ask/questions/{question_id}/{page_number}?sort=SUBMIT_DATE'  # noqa: E501

    class Meta:
        unique_together = ('asin', 'region')

    def __str__(self):
        return f'[{self.asin} - {self.get_region_display()}] {self.title}'


class Scrape(BaseModel):
    id = UUIDField(default=uuid4, primary_key=True, editable=False)
    message = CharField(max_length=200, null=True, blank=True)
    message_answers = CharField(max_length=200, null=True, blank=True)
    message_questions = CharField(max_length=200, null=True, blank=True)
    message_reviews = CharField(max_length=200, null=True, blank=True)
    product = ForeignKey(Product, related_name='scrapes', on_delete=CASCADE)
    status = PositiveSmallIntegerField(choices=ScrapeStatus.CHOICES, default=ScrapeStatus.WAITING)  # noqa: E501
    status_answers = PositiveSmallIntegerField(choices=ScrapeStatus.CHOICES, default=ScrapeStatus.WAITING)  # noqa: E501
    status_questions = PositiveSmallIntegerField(choices=ScrapeStatus.CHOICES, default=ScrapeStatus.WAITING)  # noqa: E501
    status_reviews = PositiveSmallIntegerField(choices=ScrapeStatus.CHOICES, default=ScrapeStatus.WAITING)  # noqa: E501

    def __str__(self):
        return f'[{self.get_status_display()}] {self.product}'


class Profile(BaseModel):
    id = CharField(max_length=50, primary_key=True)
    name = CharField(max_length=50)

    def __str__(self):
        return f'[{self.id}] {self.name}'


class Review(BaseModel):
    date = DateField()
    id = CharField(max_length=20, primary_key=True)
    product = ForeignKey(Product, related_name='reviews', on_delete=CASCADE)
    profile = ForeignKey(Profile, related_name='reviews', on_delete=CASCADE)
    rating = IntegerField(default=0)
    text = TextField()
    title = CharField(max_length=500)

    def __str__(self):
        return f'[{self.id}] {self.title}'


class Question(BaseModel):
    answer_count = IntegerField()
    date = DateField()
    id = CharField(max_length=20, primary_key=True)
    product = ForeignKey(Product, related_name='questions', on_delete=CASCADE)
    profile = ForeignKey(Profile, related_name='questions', on_delete=CASCADE)
    text = TextField()
    vote_count = IntegerField()

    def answers_url(self, page_number=1):
        return self.product.answers_url(self.id, page_number)

    def __str__(self):
        return f'[{self.id}] {self.text}'


class Answer(BaseModel):
    date = DateField()
    id = CharField(max_length=20, primary_key=True)
    profile = ForeignKey(Profile, related_name='answers', on_delete=CASCADE)
    question = ForeignKey(Question, related_name='answers', on_delete=CASCADE)
    text = TextField()
    vote_count = IntegerField()

    def __str__(self):
        return f'[{self.id}] {self.text}'
