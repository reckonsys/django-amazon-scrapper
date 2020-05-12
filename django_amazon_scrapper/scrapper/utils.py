from django_amazon_scrapper.scrapper.choices import AmazonRegion
from django_amazon_scrapper.scrapper.parsers import base

AR = AmazonRegion
AMAZON_PREFIX = 'https://www.amazon'

TLD_MAP = {
    AR.AU: "com.au",
    AR.BR: "com.br",
    AR.CN: "cn",
    AR.FR: "fr",
    AR.DE: "de",
    AR.IN: "in",
    AR.IT: "it",
    AR.JP: "co.jp",
    AR.MX: "com.mx",
    AR.NL: "nl",
    AR.SG: "sg",
    AR.ES: "es",
    AR.TR: "com.tr",
    AR.AE: "ae",
    AR.UK: "co.uk",
    AR.US: "com",
}

PARSER_MAP = {
    AR.AU: base,
    AR.BR: base,
    AR.CN: base,
    AR.FR: base,
    AR.DE: base,
    AR.IN: base,
    AR.IT: base,
    AR.JP: base,
    AR.MX: base,
    AR.NL: base,
    AR.SG: base,
    AR.ES: base,
    AR.TR: base,
    AR.AE: base,
    AR.UK: base,
    AR.US: base,
}

for value, _ in AR.CHOICES:
    if value not in TLD_MAP:
        raise ValueError(f'{value} ({_}) not found in TLD_MAP')

for value, _ in AR.CHOICES:
    if value not in PARSER_MAP:
        raise ValueError(f'{value} ({_}) not found in PARSER_MAP')
