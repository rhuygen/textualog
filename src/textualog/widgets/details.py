from typing import Optional

from rich.panel import Panel
from rich.text import Text
from textual.widget import Widget
from textual.reactive import Reactive

from textualog import styles
from textualog.renderables.logrecord import LogRecord


class Details(Widget):

    record: Reactive[LogRecord] = Reactive(None)

    def __init__(self):
        super().__init__()
        self.record: Optional[LogRecord] = None

    def set(self, record: LogRecord):
        self.record = record

    def render(self) -> Panel:
        return Panel(
            self._generate_renderable(),
            title="[bold]Record Details[/]",
            border_style=styles.BORDER_FOCUSED,
            box=styles.BOX,
            title_align="left",
            padding=0,
        )

    def _generate_renderable(self) -> Text:

        if self.record is None:
            return Text()

        record = Text(no_wrap=True)
        record.append(f"level      = {self.record.level}\n")
        record.append(f"process    = {self.record.process}\n")
        record.append(f"process ID = {self.record.process_id}\n")
        record.append(f"caller     = {self.record.caller}\n")
        record.append(f"msg        = {self.record.msg}\n")
        record.append(f"extra      = {self.record.extra}\n")

        return record
