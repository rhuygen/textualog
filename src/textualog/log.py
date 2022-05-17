import datetime
import logging

LOG_FORMAT_KEY_VALUE = (
    "level=%(levelname)s "
    "ts=%(asctime)s "
    "process=%(processName)s "
    "process_id=%(process)s "
    "caller=%(name)s:%(lineno)s "
    "msg=\"%(message)s\""
)

LOG_FORMAT_DATE = "%Y-%m-%dT%H:%M:%S,%f"


class DateTimeFormatter(logging.Formatter):

    def formatTime(self, record, datefmt=None):
        converted_time = datetime.datetime.fromtimestamp(record.created)
        if datefmt:
            return converted_time.strftime(datefmt)
        formatted_time = converted_time.strftime("%Y-%m-%dT%H:%M:%S")
        return f"{formatted_time}.{record.msecs:03.0f}"


def setup_logging(filename: str):
    file_formatter = DateTimeFormatter(fmt=LOG_FORMAT_KEY_VALUE, datefmt=LOG_FORMAT_DATE)
    file_handler = logging.FileHandler(filename=filename)
    file_handler.formatter = file_formatter
    file_handler.level = logging.DEBUG
    try:
        # The first default handler is the StreamHandler <stderr>
        logging.getLogger().handlers[0].level = logging.ERROR
    except IndexError:
        pass
    logging.getLogger().addHandler(file_handler)
    logging.getLogger().level = logging.DEBUG
