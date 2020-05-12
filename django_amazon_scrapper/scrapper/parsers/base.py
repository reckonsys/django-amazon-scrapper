from re import compile
from parsel.selector import Selector

non_numeric = compile('[^0-9\.]+')  # noqa: W605


def rating_transform(text):
    return text.split(' ')[0]


class Parser:

    def __init__(self, text):
        self.selector = Selector(text)

    def get_text(self, selector, transform=None):
        text = self.selector.css(f'{selector}::text').get()
        if text:
            text = text.strip()
            if transform is not None:
                text = transform(text)
            return text
        return None

    def get_int(self, selector, transform=None):
        text = self.get_text(selector, transform)
        if text is None:
            return 0
        text = non_numeric.sub('', text)
        return int(text)

    def get_float(self, selector, transform=None):
        text = self.get_text(selector, transform)
        if text is None:
            return 0.0
        text = non_numeric.sub('', text)
        return float(text)


class ProductParser(Parser):
    sel_price = '#priceblock_ourprice'
    sel_question_count = '#askATFLink span'
    sel_rating = '.a-icon.a-icon-star span'
    sel_review_count = '#acrCustomerReviewText'
    sel_title = '#productTitle'

    @property
    def price(self):
        return self.get_float(self.sel_price)

    @property
    def question_count(self):
        return self.get_int(self.sel_question_count)

    @property
    def rating(self):
        return self.get_float(self.sel_rating, rating_transform)

    @property
    def review_count(self):
        return self.get_int(self.sel_review_count)

    @property
    def title(self):
        return self.get_text(self.sel_title)


class ProfileParser(Parser):

    @property
    def id(self):
        pass

    @property
    def name(self):
        pass


class ReviewParser(Parser):

    @property
    def date(self):
        pass

    @property
    def profile_id(self):
        pass

    @property
    def rating(self):
        pass

    @property
    def text(self):
        pass

    @property
    def title(self):
        pass


class QuestionParser(Parser):

    @property
    def date(self):
        pass

    @property
    def id(self):
        pass

    @property
    def profile_id(self):
        pass

    @property
    def text(self):
        pass


class AnswerParser(Parser):

    @property
    def date(self):
        pass

    @property
    def id(self):
        pass

    @property
    def profile_id(self):
        pass

    @property
    def text(self):
        pass
