# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task

from django_amazon_scrapper.scrapper.choices import ProductStatus, ScrapeStatus
from django_amazon_scrapper.scrapper.models import Asin, Product, Scrape


@shared_task
def init_asin(asin_id):
    '''
    initialize Asin Model
    '''
    asin = Asin.objects.get(id=asin_id)
    print(f'echo asin: {asin}')


@shared_task
def init_product(product_id):
    '''
    initialize Asin Model
    '''
    product = Product.objects.get(id=product_id)
    if product.status != ProductStatus.NEWLY_ADDED:
        return
    print(f'echo product: {product_id}')


@shared_task
def init_scrape(scrape_id):
    '''
    initialize Asin Model
    '''
    scrape = Scrape.objects.get(id=scrape_id)
    if scrape.status != ScrapeStatus.WAITING:
        return
    print(f'echo scrape: {scrape_id}')
