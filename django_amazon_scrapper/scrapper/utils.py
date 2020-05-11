from django_amazon_scrapper.scrapper.choices import AmazonRegion


AR = AmazonRegion
AMAZON_PREFIX = 'https://amazon'

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

for value, _ in AR.CHOICES:
    if value not in TLD_MAP:
        raise ValueError(f'{value} ({_}) not found in TLD_MAP')
