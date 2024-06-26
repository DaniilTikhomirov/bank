from src.time import range_time, find_range_time, find_time_of_day
import pytest


@pytest.mark.parametrize('correct, date', (['Доброе утро', '2018-01-10 8:8:8'],
                                           ['Добрый день', '2018-01-10 13:13:13'],
                                           ['Добрый вечер', '2018-01-10 18:18:18'],
                                           ['Доброй ночи', '2018-01-10 2:2:2']))
def test_find_time_of_day(correct: str, date: str) -> None:
    assert find_time_of_day(date) == correct


def test_range_time() -> None:
    assert range_time('2018-01-10 8:8:8') == ['01 10 2018',
                                              '01 09 2018',
                                              '01 08 2018',
                                              '01 07 2018',
                                              '01 06 2018',
                                              '01 05 2018',
                                              '01 04 2018',
                                              '01 03 2018',
                                              '01 02 2018',
                                              '01 01 2018']


def test_find_range_time() -> None:
    data = [{'Дата платежа': '11.01.2018'},
            {'Дата платежа': '12.01.2018'},
            {'Дата платежа': '10.01.2018'},
            {'Дата платежа': '9.01.2018'},
            {'Дата платежа': '8.01.2018'},
            {'Дата платежа': '7.01.2018'},
            {'Дата платежа': '6.01.2018'},
            {'Дата платежа': '5.01.2018'}, ]
    list_time = ['01 10 2018',
                 '01 09 2018',
                 '01 08 2018',
                 '01 07 2018',
                 '01 06 2018',
                 '01 05 2018',
                 '01 04 2018',
                 '01 03 2018',
                 '01 02 2018',
                 '01 01 2018']
    assert find_range_time(data, list_time) == [{'Дата платежа': '10.01.2018'},
                                                {'Дата платежа': '9.01.2018'},
                                                {'Дата платежа': '8.01.2018'},
                                                {'Дата платежа': '7.01.2018'},
                                                {'Дата платежа': '6.01.2018'},
                                                {'Дата платежа': '5.01.2018'}]
