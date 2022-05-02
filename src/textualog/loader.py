from itertools import islice
from typing import List

from rich.text import Text

from .renderables.logrecord import LevelName
from .renderables.logrecord import LogRecord
from .widgets.levels import Levels

DEFAULT_NUM_LINES = 100
MAX_NUM_LINES = 100_000


# KeyValueLoader is a class that loads log files that have a key-value format.
# The following key-value pairs are expected in this order:
#
# level=<LEVEL>
# ts=<DATE TIME> in the format %Y-%m-%dT%H:%M:%S,%f e.g. 2022-04-08T10:52:20,371211
# process=<process name>
# process_id=<process ID>
# caller=<module>:<lineno>
# msg="<message>"

class KeyValueLoader:
    def __init__(self, filename: str):
        self.filename = filename
        self._lines: List[str] = ...
        """The original lines read from the log file."""
        self._size = 0
        """The number of lines in the log file."""
        self._records = []
        """Processed lines"""
        self._offset = 0
        """The line number of the first record, i.e. which line in the log file."""

    def load(self):
        """Loads the complete log file in a list of strings."""
        with open(self.filename, 'r') as fd:
            self._lines = fd.read().split('\n')

        self._size = len(self._lines)

    def size(self) -> int:
        """Returns the total number of lines in the log file."""
        return self._size

    def process(self, start: int = 0, num_lines: int = DEFAULT_NUM_LINES, levels: Levels = None):
        """Process a number of lines and creates a list of Records for those lines."""

        # * could keep track of those line that have been processed -> no need to process again
        # * sub_messages are e.g. Traceback or multiline messages

        self._offset = start

        sub_message: List[str] = []
        in_sub_message = False
        records = []
        match_count = 0
        for count, line in enumerate(islice(self._lines, start, None)):
            if count > MAX_NUM_LINES:
                break
            if not line.startswith("level="):
                in_sub_message = True
                sub_message.append(line)
                continue
            if in_sub_message:
                # print('\n'.join(sub_message))
                sub_message = []
                in_sub_message = False

            level, ts, process, process_id, caller, msg = line.split(maxsplit=5)
            level = LevelName[level[6:]].value

            if levels is None or levels.is_on(level):

                record = LogRecord(
                    level=level,
                    ts=ts[3:],
                    process=process[8:],
                    process_id=process_id[11:],
                    caller=caller[7:],
                    msg=msg[5:-1]  # also removes the double quotes around the message
                )

                records.append(record)
                match_count += 1

            if match_count >= num_lines:
                break

        # if sub_message:
        #     print('\n'.join(sub_message))

        self._records = records

    def __str__(self):
        return "\n".join(self._records)

    def reprocess(self, start: int, num_lines: int, levels: Levels):
        # start and stop are line numbers of the log file

        # item is the correct mapping of the requested lines in the self._records list.
        #
        # if not 0 < start - offset < len(self._records) -> reprocess the lines
        # if not 0 < start + num_lines - offset < len(self._records) -> reprocess the lines

        nr_records = len(self._records)

        if not 0 <= start - self._offset < nr_records or \
                not 0 < start + num_lines - self._offset <= nr_records:
            self.process(start, num_lines, levels)

    def get_records(self,
                    start: int = 0,
                    num_lines: int = DEFAULT_NUM_LINES,
                    levels: Levels = None) -> List[LogRecord]:

        self.process(start, num_lines, levels)

        return self._records

    def get_text(self, start: int = 0, num_lines: int = DEFAULT_NUM_LINES, levels: Levels = None) -> Text:

        self.process(start, num_lines, levels)

        record: LogRecord
        text = Text()
        [
            text.append(record.__rich__()).append('\n')
            for record in self._records
        ]
        return text


if __name__ == "__main__":

    fn = '/Users/rik/Desktop/general.log'
    fn = '/Users/rik/data/CSL/log/general.log.2022-04-08'
    fn = '/Users/rik/data/CSL/log/general.log'

    loader = KeyValueLoader(fn)
    loader.load()
    loader.process(0, 20, None)

    import rich
    rich.print(loader.get_text(0, 20))
    rich.print("---")
    rich.print(loader.get_text(2, 4))
    rich.print("---")
    rich.print(loader.get_text(18, 2))
    rich.print("---")
    rich.print(loader.get_text(20, 2))
