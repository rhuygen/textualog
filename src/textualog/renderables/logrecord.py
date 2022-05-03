import datetime
import logging
import time
from enum import Enum
from typing import Union

import rich
from rich.text import Text


class LevelColor(Enum):
    DEBUG = "white"
    INFO = "green"
    WARNING = "orange3"
    ERROR = "red"
    CRITICAL = "bright_magenta"


class LevelName(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class LogRecord:
    def __init__(
            self,
            msg: str,
            level: int = logging.INFO,
            created: float = None,
            ts: str = None,
            process: str = None,
            caller: str = None,
            process_id: int = None,
            selected: bool = False,
            **kwargs
    ):
        self.msg = msg
        self.level = level
        self.ts = ts
        self.created = created or to_timestamp(self.ts) if self.ts else time.time()
        self.process = process
        self.caller = caller
        self.process_id = process_id
        self.selected = selected

    def __str__(self) -> str:
        text = (
            f"level={self.level} "
            f"ts={format_datetime(datetime.datetime.fromtimestamp(self.created))} "
            f"msg=\"{self.msg}\""
        )
        return text

    def get_text(self) -> Text:
        color = LevelColor[LevelName(self.level).name].value
        return Text(
            f"{format_datetime(from_timestamp(self.created))} "
            f"{LevelName(self.level).name} "
            f"{self.msg}",
            style=f"{color} {'on grey93' if self.selected else ''}"
        )

    def __rich__(self) -> Text:
        color = LevelColor[LevelName(self.level).name].value
        return Text(
            f"{format_datetime(from_timestamp(self.created))} "
            f"{LevelName(self.level).name} "
            f"{self.msg}",
            style=f"{color}"
        )


def format_datetime(dt: Union[str, datetime.datetime] = None, fmt: str = None, width: int = 6, precision: int = 3):
    """Format a datetime as YYYY-mm-ddTHH:MM:SS.μs+0000.

    If the given argument is not timezone aware, the last part, i.e. `+0000` will not be there.

    If no argument is given, the timestamp is generated as
    `datetime.datetime.now(tz=datetime.timezone.utc)`.

    The `dt` argument can also be a string with the following values: today, yesterday, tomorrow,
    and 'day before yesterday'. The format will then be '%Y%m%d' unless specified.

    Optionally, a format string can be passed in to customize the formatting of the timestamp.
    This format string will be used with the `strftime()` method and should obey those conventions.

    Example:
        >>> format_datetime(datetime.datetime(2020, 6, 13, 14, 45, 45, 696138))
        '2020-06-13T14:45:45.696'
        >>> format_datetime(datetime.datetime(2020, 6, 13, 14, 45, 45, 696138), precision=6)
        '2020-06-13T14:45:45.696138'
        >>> format_datetime(datetime.datetime(2020, 6, 13, 14, 45, 59, 999501), precision=3)
        '2020-06-13T14:45:59.999'
        >>> format_datetime(datetime.datetime(2020, 6, 13, 14, 45, 59, 999501), precision=6)
        '2020-06-13T14:45:59.999501'
        >>> _ = format_datetime()
        ...
        >>> format_datetime("yesterday")
        '20220214'
        >>> format_datetime("yesterday", fmt="%d/%m/%Y")
        '14/02/2022'

    Args:
        dt (datetime): a datetime object or an agreed string like yesterday, tomorrow, ...
        fmt (str): a format string that is accepted by `strftime()`
        width (int): the width to use for formatting the microseconds
        precision (int): the precision for the microseconds
    Returns:
        a string representation of the current time in UTC, e.g. `2020-04-29T12:30:04.862+0000`.

    Raises:
        A ValueError will be raised when the given dt argument string is not understood.
    """
    dt = dt or datetime.datetime.now(tz=datetime.timezone.utc)
    if isinstance(dt, str):
        fmt = fmt or "%Y%m%d"
        if dt.lower() == "yesterday":
            dt = datetime.date.today() - datetime.timedelta(days=1)
        elif dt.lower() == "today":
            dt = datetime.date.today()
        elif dt.lower() == "day before yesterday":
            dt = datetime.date.today() - datetime.timedelta(days=2)
        elif dt.lower() == "tomorrow":
            dt = datetime.date.today() + datetime.timedelta(days=1)
        else:
            raise ValueError(f"Unknown date passed as an argument: {dt}")

    if fmt:
        timestamp = dt.strftime(fmt)
    else:
        width = min(width, precision)
        timestamp = (
            f"{dt.strftime('%Y-%m-%dT%H:%M')}:"
            f"{dt.second:02d}.{dt.microsecond//10**(6-precision):0{width}d}{dt.strftime('%z')}"
        )

    return timestamp


def from_timestamp(ts: float):
    return datetime.datetime.fromtimestamp(ts)


def to_timestamp(ts: str):
    return datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S,%f').timestamp()


if __name__ == "__main__":

    for level in LevelName:
        record = LogRecord(level=level.value,
                           msg=f"A simple {level.name} message should be printed in {LevelColor[level.name].value}.")
        print(record)
        rich.print(record)
