from django.conf import settings

from django_amazon_scrapper.scrapper.choices import AmazonRegion

if hasattr(settings, 'SCRAPE_AMAZON_REGIONS'):
    SCRAPE_AMAZON_REGIONS = settings.SCRAPE_AMAZON_REGIONS
else:
    SCRAPE_AMAZON_REGIONS = [AmazonRegion.US]

_regions = [val for val, label in AmazonRegion.CHOICES]

for region in SCRAPE_AMAZON_REGIONS:
    if region not in _regions:
        raise ValueError(f'Unknown AmazonRegion ({region})')
