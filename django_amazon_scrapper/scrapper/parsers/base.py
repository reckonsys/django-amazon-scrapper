from re import compile
from datetime import datetime

from parsel.selector import Selector

from django_amazon_scrapper.scrapper.config import (
    MAX_ANSWER_PAGES, MAX_QUESTION_PAGES, MAX_REVIEW_PAGES)

non_numeric = compile('[^0-9\.]+')  # noqa: W605


def rating_transform(text):
    return text.split(' ')[0]


def date_transform(text):
    return text.split(' on ')[1]


class Parser:

    def __init__(self, text_or_selector):
        if isinstance(text_or_selector, str):
            self.selector = Selector(text_or_selector)
        else:
            self.selector = text_or_selector

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

    def get_date(self, selector, transform=None):
        text = self.get_text(selector, transform)
        if text is None:
            return None
        return datetime.strptime(text, '%B %d, %Y').date()


class ListMixin:
    max_pages = 0
    count_selector = ''

    @property
    def count_max(self):
        return self.max_pages * 10

    @property
    def counter(self):
        text = self.get_text(self.count_selector)
        if text is None:
            return 0, 0
        text_split = text.split(' ')
        if len(text_split) != 5:
            return 0, 0
        _, _range, _, total, _ = text_split
        count_end = int(non_numeric.sub('', _range.split('-')[1]))
        count_total = int(non_numeric.sub('', total))
        return count_end, count_total

    @property
    def is_final(self):
        end, total = self.counter
        return end == total or end == self.count_max


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
    sel_date = '.review-date'
    sel_profile_id = '.a-profile'
    sel_profile_name = '.a-profile-name'
    sel_rating = '.review-rating span'
    sel_text = '.review-text span'
    sel_title = '.review-title span'

    @property
    def id(self):
        return self.selector.attrib.get('id')

    @property
    def date(self):
        return self.get_date(self.sel_date, date_transform)

    @property
    def profile_id(self):
        return self.selector.css(self.sel_profile_id).attrib.get('href').split('/')[3]  # noqa: E501

    @property
    def profile_name(self):
        return self.get_text(self.sel_profile_name)

    @property
    def rating(self):
        return self.get_float(self.sel_rating, rating_transform)

    @property
    def text(self):
        return self.get_text(self.sel_text)

    @property
    def title(self):
        return self.get_text(self.sel_title)


class ReviewListParser(Parser, ListMixin):
    count_selector = '#filter-info-section span'
    max_pages = MAX_REVIEW_PAGES
    sel_review = '.review'

    @property
    def reviews(self):
        return [ReviewParser(selector) for selector in self.selector.css(self.sel_review)]  # noqa: E501


class QuestionParser(Parser):

    @property
    def date(self):
        pass

    @property
    def id(self):
        pass

    @property
    def profile(self):
        pass

    @property
    def text(self):
        pass


class QuestionListParser(Parser, ListMixin):
    count_selector = '.a-section.askPaginationHeaderMessage span'
    max_pages = MAX_QUESTION_PAGES

    @property
    def questions(self):
        pass


class AnswerParser(Parser):

    @property
    def date(self):
        pass

    @property
    def id(self):
        pass

    @property
    def profile(self):
        pass

    @property
    def text(self):
        pass


class AnswerListParser(Parser, ListMixin):
    count_selector = '.a-spacing-large.a-color-secondary'
    max_pages = MAX_ANSWER_PAGES

    @property
    def answers(self):
        pass
