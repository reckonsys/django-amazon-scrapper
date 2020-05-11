from orm_choices import choices


@choices
class ProductStatus:
    class Meta:
        NEWLY_ADDED = (1, 'Newly Added')
        INVALID = (2, 'Invalid')
        VALID = (3, 'Valid')


@choices
class AmazonRegion:
    class Meta:
        AU = (1, 'Australia')
        BR = (2, 'Brazil')
        CN = (3, 'China')
        FR = (4, 'France')
        DE = (5, 'Germany')
        IN = (6, 'India')
        IT = (7, 'Italy')
        JP = (8, 'Japan')
        MX = (9, 'Mexico')
        NL = (10, 'Netherland')
        SG = (11, 'Singapore')
        ES = (12, 'Spain')
        TR = (13, 'Turkey')
        AE = (14, 'Arab Emirates')
        UK = (15, 'United Kingdom')
        US = (16, 'United States')


@choices
class ScrapeStatus:
    class Meta:
        WAITING = (1, 'Waiting')
        SCRAPPING = (2, 'Scrapping')
        FAILED = (3, 'Failed')
        CREATED = (4, 'Created')
        UPDATED = (5, 'Updated')
