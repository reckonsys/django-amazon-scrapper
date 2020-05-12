from celery import current_app
from django.db.models.signals import post_save

from django_amazon_scrapper.scrapper import signals  # noqa: F401
from django_amazon_scrapper.scrapper.choices import ProductStatus, ScrapeStatus
from django_amazon_scrapper.scrapper.models import Asin, Product, Scrape

PREFIX = 'django_amazon_scrapper.scrapper.tasks'


def save_asin(sender, instance, **kwargs):
    if not instance.is_active:
        return
    return current_app.send_task(f'{PREFIX}.init_asin', (instance.id, ))


def save_product(sender, instance, **kwargs):
    if instance.status != ProductStatus.NEWLY_ADDED:
        return
    return current_app.send_task(f'{PREFIX}.init_product', (instance.id, ))


def save_scrape(sender, instance, **kwargs):
    if instance.status != ScrapeStatus.WAITING:
        return
    return current_app.send_task(f'{PREFIX}.init_scrape', (instance.id, ))


post_save.connect(save_asin, sender=Asin)
post_save.connect(save_product, sender=Product)
post_save.connect(save_scrape, sender=Scrape)
