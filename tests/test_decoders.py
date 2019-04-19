from datetime import date, datetime, time, timedelta, timezone
from enum import Enum
from uuid import UUID

import pytest
import pytz

from pytcher.unmarshallers import decode


class Color(Enum):
    RED = 1
    GREEN = 2


@pytest.mark.parametrize(
    "test_input, obj_type, expected",
    [
        ('RED', Color, Color.RED),
        ('2019-02-01T04:03:01.000000', datetime, datetime(2019, 2, 1, 4, 3, 1)),
        ('2019-02-01T04:03:01.000000-0800', datetime, pytz.timezone('US/Pacific').localize(datetime(2019, 2, 1, 4, 3, 1))),
        ('2019-02-01', date, date(2019, 2, 1)),
        ('13:43:12.000000', time, time(13, 43, 12)),
        ('US/Pacific', timezone, pytz.timezone('US/Pacific')),
        ('P2DT10H27M12.000034S', timedelta, timedelta(days=2, hours=10, minutes=27, seconds=12, microseconds=34)),
        ('7e7bcd85-920c-456d-911c-7a4ad2b242e7', UUID, UUID('7e7bcd85-920c-456d-911c-7a4ad2b242e7'))

    ]
)
def test_default_decoders(test_input, obj_type, expected):
    assert expected == decode(obj_type, test_input)
