from celery import current_app
from django.db.models.signals import post_save

from django_amazon_scrapper.scrapper import signals  # noqa: F401
from django_amazon_scrapper.scrapper.models import Asin, Product, Scrape

PREFIX = 'django_amazon_scrapper.scrapper.tasks'


def save_asin(sender, asin, **kwargs):
    return current_app.send_task(f'{PREFIX}.init_asin', (asin.id, ))


def save_product(sender, product, **kwargs):
    return current_app.send_task(f'{PREFIX}.init_product', (product.id, ))


def save_scrape(sender, scrape, **kwargs):
    return current_app.send_task(f'{PREFIX}.init_scrape', (scrape.id, ))


post_save.connect(save_asin, sender=Asin)
post_save.connect(save_product, sender=Product)
post_save.connect(save_scrape, sender=Scrape)
