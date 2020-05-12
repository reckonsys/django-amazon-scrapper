from django.conf import settings

from django_amazon_scrapper.scrapper.choices import AmazonRegion

MAX_ANSWER_PAGES = 100
MAX_QUESTION_PAGES = 100
MAX_REVIEW_PAGES = 500
TASKS = 'django_amazon_scrapper.scrapper.tasks'


if hasattr(settings, 'SCRAPE_AMAZON_REGIONS'):
    SCRAPE_AMAZON_REGIONS = settings.SCRAPE_AMAZON_REGIONS
else:
    SCRAPE_AMAZON_REGIONS = [AmazonRegion.US]

_regions = [val for val, label in AmazonRegion.CHOICES]

for region in SCRAPE_AMAZON_REGIONS:
    if region not in _regions:
        raise ValueError(f'Unknown AmazonRegion ({region}) in SCRAPE_AMAZON_REGIONS')  # noqa: E501
