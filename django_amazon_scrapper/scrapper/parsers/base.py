from parsel.selector import Selector


class Parser:

    def __init__(self, text):
        self.selector = Selector(text)


class ProductParser(Parser):

    @property
    def id(self):
        pass

    @property
    def name(self):
        pass

    @property
    def price(self):
        pass

    @property
    def qna_count(self):
        pass

    @property
    def rating(self):
        pass

    @property
    def rating_count(self):
        pass


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
