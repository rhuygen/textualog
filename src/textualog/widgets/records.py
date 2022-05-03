from __future__ import annotations

from typing import List
from typing import Optional

from rich.console import ConsoleRenderable
from rich.panel import Panel
from rich.text import Text
from textual import events
from textual.reactive import Reactive
from textual.widget import Widget

from .. import styles
from ..renderables.logrecord import LogRecord

PANEL_SIZE = 10


class Records(Widget):

    height: Reactive[int | None] = Reactive(None)

    def __init__(self, height: int | None = None):
        super().__init__()
        self.height = height
        self.records: List[LogRecord] = [
            # LogRecord(level=logging.INFO,
            #           msg="The log messages will be displayed here as a list or table.")
        ]
        self._selected_idx: Optional[int] = None

    async def on_mount(self) -> None:
        # self.layout_size = PANEL_SIZE
        # self.layout_fraction = 1
        ...

    async def on_click(self, event: events.Click) -> None:

        if self._selected_idx is not None:
            self.records[self._selected_idx].selected = False

        idx = event.y - 1  # Records is a Panel with the header as the first line

        try:
            record = self.records[idx]
            self.app.record_info.set(record)
            record.selected = True
            self._selected_idx = idx
            self.refresh(repaint=True)
        except IndexError:
            pass

    def render(self) -> Panel:
        return Panel(
            self._generate_renderable(),
            title="[bold]Records[/]",
            border_style=styles.BORDER_FOCUSED,
            box=styles.BOX,
            title_align="left",
            padding=0,
            height=self.height,
        )

    def replace(self, records: List[LogRecord]):
        self.records = records
        self._selected_idx = None

    def update(self, records: List[LogRecord]):
        self.records.extend(records)
        self._selected_idx = None

    def _generate_renderable(self) -> ConsoleRenderable:
        text = Text(no_wrap=True)
        [
            text.append(record.get_text()).append("\n")
            for record in self.records
        ]
        return text
