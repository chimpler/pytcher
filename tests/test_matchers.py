from pytcher import Choice, Float, Integer, NoMatch


def test_matcher_integer():
    assert 5 == Integer().match(5)
    assert 15 == Integer(10, 20).match('15')
    assert Integer(10, 20).match('9') is NoMatch
    assert Integer(10, 20).match('21') is NoMatch
    assert Integer(10, 20).match('15.5') is NoMatch
    assert Integer().match('') is NoMatch


def test_matcher_float():
    assert 5 == Float().match(5)
    assert 5.2 == Float().match(5.2)
    assert Float(10, 20).match('9.2') is NoMatch
    assert Float(10, 20).match('21') is NoMatch
    assert 15.5 == Float(10, 20).match('15.5')
    assert 15 == Float(10, 20).match('15')


def test_matcher_choice_case_sensitive():
    choice = Choice('books', 'novels', ignore_case=False)
    assert 'books' == choice.match('books')
    assert 'novels' == choice.match('novels')
    assert choice.match('') is NoMatch
    assert choice.match('Books') is NoMatch
    assert choice.match('Novels') is NoMatch


def test_matcher_choice_non_case_sensitive():
    choice = Choice('books', 'novels', ignore_case=True)
    assert 'books' == choice.match('books')
    assert 'novels' == choice.match('novels')
    assert choice.match('') is NoMatch
    assert 'books' == choice.match('Books')
    assert 'novels' == choice.match('Novels')
