from datetime import datetime, date, time, timedelta, timezone
from enum import Enum
from uuid import UUID

import pytz

from pytcher.unmarshallers import decode


def test_default_decoders():
    class Color(Enum):
        RED = 1
        GREEN = 2

    assert Color.RED == decode(Color, 'RED')
    assert datetime(2019, 2, 1, 4, 3, 1) == decode(datetime, '2019-02-01T04:03:01.000000')
    assert pytz.timezone('US/Pacific').localize(datetime(2019, 2, 1, 4, 3, 1)) == decode(datetime, '2019-02-01T04:03:01.000000-0800')
    assert date(2019, 2, 1) == decode(date, '2019-02-01')
    assert time(13, 43, 12) == decode(time, '13:43:12.000000')
    assert pytz.timezone('US/Pacific') == decode(timezone, 'US/Pacific')
    assert timedelta(days=2, hours=10, minutes=27, seconds=12, microseconds=34) == decode(timedelta, 'P2DT10H27M12.000034S')
    assert UUID('7e7bcd85-920c-456d-911c-7a4ad2b242e7') == decode(UUID, '7e7bcd85-920c-456d-911c-7a4ad2b242e7')
