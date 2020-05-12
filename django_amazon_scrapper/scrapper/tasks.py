# Create your tasks here
from __future__ import absolute_import, unicode_literals

import requests
from celery import shared_task

from django_amazon_scrapper.scrapper.choices import ProductStatus, ScrapeStatus
from django_amazon_scrapper.scrapper.config import SCRAPE_AMAZON_REGIONS
from django_amazon_scrapper.scrapper.models import Asin, Product, Scrape

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
    initialize Asin Model
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
    initialize Asin Model
    '''
    scrape = Scrape.objects.get(id=scrape_id)
    scrape.status = ScrapeStatus.SCRAPPING
    scrape.save()
