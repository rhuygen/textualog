import logging
import time

from textualog.renderables.record import LogRecord


def test_simple_construction():

    msg = "A simple log message"
    record = LogRecord(msg)

    assert record.created <= time.time()
    assert record.msg == msg
    assert record.level == logging.INFO
