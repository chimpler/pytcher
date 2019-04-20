import pytest

from pytcher import Choice, Float, Integer, NoMatch, Regex


@pytest.mark.parametrize(
    "test_input, matcher, expected",
    [
        (5, Integer(), 5),
        ('15', Integer(), 15),
        ('9', Integer(10, 20), NoMatch),
        ('21', Integer(10, 20), NoMatch),
        ('16', Integer(10, 20), 16),
        ('15.5', Integer(10, 20), NoMatch),
        ('', Integer(10, 20), NoMatch)
    ]
)
def test_matcher_integer(test_input, matcher, expected):
    assert expected == matcher.match(test_input)


@pytest.mark.parametrize(
    "test_input, matcher, expected",
    [
        (5, Float(), 5),
        ('15', Float(), 15),
        ('9', Float(10, 20), NoMatch),
        ('21', Float(10, 20), NoMatch),
        ('16', Float(10, 20), 16),
        ('15.5', Float(10, 20), 15.5),
        ('', Float(10, 20), NoMatch)
    ]
)
def test_matcher_float(test_input, matcher, expected):
    assert expected == matcher.match(test_input)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ('books', 'books'),
        ('novels', 'novels'),
        ('', NoMatch),
        ('books', 'books'),
        ('Books', NoMatch),
        ('Novels', NoMatch),
    ]
)
def test_matcher_choice_case_sensitive(test_input, expected):
    choice = Choice('books', 'novels', ignore_case=False)
    assert expected == choice.match(test_input)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ('books', 'books'),
        ('novels', 'novels'),
        ('', NoMatch),
        ('books', 'books'),
        ('Books', 'books'),
        ('Novels', 'novels'),
    ]
)
def test_matcher_choice_non_case_sensitive(test_input, expected):
    choice = Choice('books', 'novels', ignore_case=True)
    assert 'books' == choice.match('books')
    assert 'novels' == choice.match('novels')
    assert choice.match('') is NoMatch
    assert 'books' == choice.match('Books')
    assert 'novels' == choice.match('Novels')


def test_matcher_simple_regex():
    regex = Regex('^a.*e$')
    assert 'apple' == regex.match('apple')
    assert regex.match('apples') is NoMatch


def test_matcher_one_group_regex():
    regex = Regex('^fruit-(?P<apple>a.*e)$')
    assert 'apple' == regex.match('fruit-apple')
    assert regex.match('fruit-apples') is NoMatch


def test_matcher_two_groups_regex():
    regex = Regex('^fruit-(?P<apple>a.*e)-(?P<orange>o.*e)$')
    assert ['apple', 'orange'] == regex.match('fruit-apple-orange')
    assert regex.match('fruit-apple-strawberry') is NoMatch
