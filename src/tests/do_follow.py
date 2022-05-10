import logging

from textualog.log import setup_logging
from textualog.system import do_every

setup_logging("test.log")

MODULE_LOGGER = logging.getLogger()


def fake_log_messages():
    MODULE_LOGGER.debug("A periodic debug message for testing.")
    MODULE_LOGGER.info("A periodic info message for testing.")
    MODULE_LOGGER.warning("A periodic warning message for testing.")
    MODULE_LOGGER.error("A periodic error message for testing.")
    MODULE_LOGGER.critical("A periodic critical message for testing.")
    try:
        raise FileNotFoundError("The file no-name.txt doesn't exist")
    except FileNotFoundError as exc:
        MODULE_LOGGER.error(f"Caught an exception: {exc}", exc_info=True)


if __name__ == "__main__":
    do_every(1.0, fake_log_messages)
