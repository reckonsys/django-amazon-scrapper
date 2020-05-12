# Create your tasks here
from __future__ import absolute_import, unicode_literals

import requests
from celery import shared_task

from django_amazon_scrapper.scrapper.choices import ProductStatus, ScrapeStatus
from django_amazon_scrapper.scrapper.config import SCRAPE_AMAZON_REGIONS
from django_amazon_scrapper.scrapper.models import Asin, Product, Scrape

# from random import choice

# UA = 'Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'  # noqa: E501
'''
desktop_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',  # noqa: E501
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',  # noqa: E501
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',  # noqa: E501
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',  # noqa: E501
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',  # noqa: E501
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',  # noqa: E501
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',  # noqa: E501
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',  # noqa: E501
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',  # noqa: E501
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',  # noqa: E501
]


def random_headers():
    return {
        'User-Agent': choice(desktop_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',  # noqa: E501
    }
'''
headers = {
    'User-Agent': UA,
    'Host': 'www.amazon.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',  # noqa: E501
}


@shared_task
def init_asin(asin_id):
    '''
    initialize Asin Model
    '''
    asin = Asin.objects.get(id=asin_id)
    for region in SCRAPE_AMAZON_REGIONS:
        asin.products.get_or_create(region=region)
    print(f'echo asin: {asin}')


@shared_task
def init_product(product_id):
    '''
    initialize Asin Model
    '''
    product = Product.objects.get(id=product_id)
    product.status = ProductStatus.VALIDATING
    product.save()
    response = requests.get(product.product_url(), headers=headers)
    if response.status_code != 200:
        product.status = ProductStatus.INVALID
        product.save()
        return
    product.status = ProductStatus.VALID
    parser = product.parser.ProductParser(response.text)
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
    print(f'echo scrape: {scrape}')
