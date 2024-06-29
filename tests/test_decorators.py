from datetime import datetime

from src.decorators import log
import pytest
from unittest.mock import patch

@log()
def a(x: int, y: int) -> int:
    return x + y


@pytest.mark.parametrize('x, y, correct', ([1, 1, ['06-30-24 00:09:21 a ok\n',
                                                   'result: 2\n',
                                                   '================================================== passed '
                                                   '==================================================\n']],
                                           [1, '1', ['06-30-24 00:09:21 a error: TypeError\n',
                                                     "full error: unsupported operand type(s) for +: 'int' and 'str'\n",
                                                     '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!TypeError!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n']]))
def test_log(x: int, y: int | str, correct: list) -> None:
    target = datetime(2024, 6, 30, 0, 9, 21)
    with patch('datetime.datetime') as mock_now:
        mock_now.now.return_value = target
        a(x, y)
        with open('log_you_func.log', 'r', encoding='utf8') as file:
            f = file.readlines()
        assert f[-3:] == correct
