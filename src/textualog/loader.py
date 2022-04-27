from enum import Enum
from typing import List

from rich.text import Text
from textualog.renderables.record import LevelName
from textualog.renderables.record import LogRecord


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
        self._records = []

    def load(self):
        """Loads the complete log file in a list of strings."""
        with open(self.filename, 'r') as fd:
            self._lines = fd.read().split('\n')

    def process(self, item: slice = slice(None, None, None)):
        """Process a number of lines and creates a list of Records for those lines."""
        # * could keep track of those line that have been processed -> no need to process again
        # * sub_messages are e.g. Traceback or multiline messages
        sub_message: List[str] = []
        in_sub_message = False
        records = []
        for line in self._lines[item]:
            if not line.startswith("level="):
                in_sub_message = True
                sub_message.append(line)
                continue
            if in_sub_message:
                # print('\n'.join(sub_message))
                sub_message = []
                in_sub_message = False

            level, ts, process, process_id, caller, msg = line.split(maxsplit=5)

            record = LogRecord(
                level=LevelName[level[6:]].value,
                ts=ts[3:],
                process=process,
                process_id=process_id,
                caller=caller,
                msg=msg[4:]
            )

            # record = logging.LogRecord(
            #     name=fn,
            #     level=logging._nameToLevel[level[6:]],
            #     pathname=__file__,
            #     lineno=caller.split(':')[1],
            #     # created=datetime.strptime(date_string=ts[3:], format="%Y-%m-%dT%H:%M:%S.%f+0000").timestamp(),
            #     msg=msg[4:],
            #     # process=process_id[11:],
            #     args=(),
            #     exc_info=None,
            #     func=None,
            #     sinfo=None
            # )
            # record._cutelog = None

            records.append(record)

        # if sub_message:
        #     print('\n'.join(sub_message))

        # print(f"{len(records)=}")

        self._records = records

    def __str__(self):
        return "\n".join(self._records)

    def __rich__(self) -> str:
        return self._get_rich_lines()

    def _get_rich_lines(self, item=slice(None, 20, None)):
        # print(f"{item=}")
        records = self._records[item] if isinstance(item, slice) else [self._records[item]]
        text = Text()
        [
            text.append(record.__rich__()).append('\n')
            for record in records
        ]
        return text

    def __getitem__(self, item):
        return self._records[item]

    @property
    def lines(self):
        parent = self

        class Lines:
            def __getitem__(self, item):
                return parent._get_rich_lines(item)

        return Lines()


if __name__ == "__main__":

    fn = '/Users/rik/Desktop/general.log'
    fn = '/Users/rik/data/CSL/log/general.log.2022-04-08'
    loader = KeyValueLoader(fn)
    loader.load()
    loader.process(slice(20))

    import rich
    rich.print(loader.lines[:4])
    rich.print("---")
    rich.print(loader[2:4])
