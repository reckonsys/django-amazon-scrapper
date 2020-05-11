from django.contrib import admin

from django_amazon_scrapper.scrapper import signals  # noqa: F401
from django_amazon_scrapper.scrapper.models import (
    Answer, Asin, Product, Profile, Question, Review, Scrape)

admin.site.register(Answer)
admin.site.register(Asin)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Review)
admin.site.register(Scrape)
