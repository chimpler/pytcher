from datetime import date, datetime, time, timedelta
from enum import Enum
from uuid import UUID

import pytest
import pytz

from pytcher.marshallers import encode


class Color(Enum):
    RED = 1
    GREEN = 2


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (Color.RED, 'RED'),
        (datetime(2019, 2, 1, 4, 3, 1), '2019-02-01T04:03:01.000000'),
        (pytz.timezone('US/Pacific').localize(datetime(2019, 2, 1, 4, 3, 1)), '2019-02-01T04:03:01.000000-0800'),
        (date(2019, 2, 1), '2019-02-01'),
        (time(13, 43, 12), '13:43:12.000000'),
        (pytz.timezone('US/Pacific'), 'US/Pacific'),
        (timedelta(days=2, hours=10, minutes=27, seconds=12, microseconds=34), 'P2DT10H27M12.000034S'),
        (UUID('7e7bcd85-920c-456d-911c-7a4ad2b242e7'), '7e7bcd85-920c-456d-911c-7a4ad2b242e7')

    ]
)
def test_default_encoders(test_input, expected):
    assert expected == encode(test_input)
