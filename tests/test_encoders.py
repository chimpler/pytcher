from datetime import datetime, date, time, timedelta
from enum import Enum
from uuid import UUID
import pytz
from pytcher.marshallers import encode


def test_default_encoders():
    class Color(Enum):
        RED = 1
        GREEN = 2

    assert 'RED' == encode(Color.RED)
    assert '2019-02-01T04:03:01.000000' == encode(datetime(2019, 2, 1, 4, 3, 1))
    assert '2019-02-01T04:03:01.000000-0800' == encode(pytz.timezone('US/Pacific').localize(datetime(2019, 2, 1, 4, 3, 1)))
    assert '2019-02-01' == encode(date(2019, 2, 1))
    assert '13:43:12.000000' == encode(time(13, 43, 12))
    assert 'US/Pacific' == encode(pytz.timezone('US/Pacific'))
    assert 'P2DT10H27M12.000034S' == encode(timedelta(days=2, hours=10, minutes=27, seconds=12, microseconds=34))
    assert '7e7bcd85-920c-456d-911c-7a4ad2b242e7' == encode(UUID('7e7bcd85-920c-456d-911c-7a4ad2b242e7'))
