from __future__ import annotations

from typing import Optional

from rich.panel import Panel
from rich.text import Text
from textual import events
from textual.reactive import Reactive
from textual.widget import Widget

from .. import styles
from ..renderables.logrecord import LogRecord

PANEL_SIZE = 5


class RecordInfo(Widget):

    record: Reactive[LogRecord] = Reactive(None)

    def __init__(self, height: int | None = None):
        super().__init__()
        self.record: Optional[LogRecord] = None

    async def on_mount(self) -> None:
        # self.layout_size = PANEL_SIZE
        # self.layout_fraction = 1
        ...

    async def on_click(self, event: events.Click) -> None:
        self.app.show_details = True

    def set(self, record: LogRecord):
        self.record = record
        self.app.details_widget.set(self.record)

    def render(self) -> Panel:

        return Panel(
            self._generate_renderable(),
            title=f"[bold]Record Info"
                  f"{' *' if self.record is not None and self.record.extra else ''}"
                  f"[/]",
            border_style=styles.BORDER_FOCUSED,
            box=styles.BOX,
            title_align="left",
            padding=0,
            # height=PANEL_SIZE,
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

        return record
