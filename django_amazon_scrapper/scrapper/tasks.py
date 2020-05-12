# Create your tasks here
from __future__ import absolute_import, unicode_literals

import requests
from celery import current_app, shared_task

from django_amazon_scrapper.scrapper.choices import ProductStatus, ScrapeStatus
from django_amazon_scrapper.scrapper.config import (
    MAX_ANSWER_PAGES, MAX_QUESTION_PAGES, MAX_REVIEW_PAGES,
    SCRAPE_AMAZON_REGIONS, TASKS)
from django_amazon_scrapper.scrapper.models import (
    Answer, Asin, Product, Profile, Question, Review, Scrape)

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'  # noqa: E501


def fetch(url):
    headers = {
        'User-Agent': UA,
        'Host': url.replace('https://', '').split('/')[0],
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',  # noqa: E501
    }
    return requests.get(url, headers=headers)


@shared_task
def init_asin(asin_id):
    '''
    initialize Asin Model
    '''
    asin = Asin.objects.get(id=asin_id)
    for region in SCRAPE_AMAZON_REGIONS:
        asin.products.get_or_create(region=region)


@shared_task
def init_product(product_id):
    '''
    initialize Product Model
    '''
    product = Product.objects.get(id=product_id)
    product.status = ProductStatus.VALIDATING
    product.save()

    response = fetch(product.product_url())
    if response.status_code != 200:
        product.status = ProductStatus.INVALID
        product.save()
        return

    parser = product.parser.ProductParser(response.text)
    if parser.title is None:
        product.status = ProductStatus.INVALID
        product.save()
        return

    product.status = ProductStatus.VALID
    product.price = parser.price
    product.question_count = parser.question_count
    product.rating = parser.rating
    product.review_count = parser.review_count
    product.title = parser.title
    product.save()
    product.scrapes.create()


@shared_task
def init_scrape(scrape_id):
    '''
    initialize Scrape Model
    '''
    scrape = Scrape.objects.get(id=scrape_id)
    scrape.status = ScrapeStatus.SCRAPPING
    scrape.save()
    current_app.send_task(f'{TASKS}.scrape_reviews', (scrape_id, ))
    current_app.send_task(f'{TASKS}.scrape_questions', (scrape_id, ))


@shared_task
def scrape_reviews(scrape_id):
    '''
    Scrape Reviews
    '''
    scrape = Scrape.objects.get(id=scrape_id)
    scrape.status_reviews = ScrapeStatus.SCRAPPING
    scrape.save()
    for page_number in range(1, MAX_REVIEW_PAGES):
        url = scrape.product.reviews_url(page_number)
        response = fetch(url)
        if response.status_code != 200:
            scrape.status_reviews = ScrapeStatus.FAILED
            scrape.message_reviews = url
            scrape.save()
            return

        parser = scrape.product.parser.ReviewListParser(response.text)

        for review in parser.reviews:
            if Review.objects.filter(id=review.id).exists():
                scrape.status_reviews = ScrapeStatus.COMPLETED
                scrape.save()
                return

            profile, _ = Profile.objects.get_or_create(id=review.profile_id)
            profile.name = review.profile_name
            profile.save()
            scrape.product.reviews.create(
                date=review.date, id=review.id, profile=profile,
                rating=review.rating, text=review.text, title=review.title)

        if parser.is_final:
            scrape.status_reviews = ScrapeStatus.COMPLETED
            scrape.save()
            return

    scrape.status_reviews = ScrapeStatus.COMPLETED
    scrape.save()


@shared_task
def scrape_questions(scrape_id):
    '''
    Scrape Questions
    '''
    scrape = Scrape.objects.get(id=scrape_id)
    scrape.status_questions = ScrapeStatus.SCRAPPING
    scrape.save()
    # current_app.send_task(f'{TASKS}.scrape_answers', (scrape_id, question.id))  # noqa: E501


@shared_task
def scrape_answers(scrape_id, question_id):
    '''
    Scrape Answers
    '''
    scrape = Scrape.objects.get(id=scrape_id)
    scrape.status_answers = ScrapeStatus.SCRAPPING
    scrape.save()
    question = Question.objects.get(id=question_id)
    print(question)
    current_app.send_task(f'{TASKS}.scrape_completed', (scrape_id, ))


@shared_task
def scrape_completed(scrape_id):
    scrape = Scrape.objects.get(id=scrape_id)
    scrape.status = ScrapeStatus.COMPLETED
    scrape.save()
