from __future__ import annotations

import logging
from typing import List

from rich.panel import Panel
from rich.text import Text
from rich.console import ConsoleRenderable
from textual.reactive import Reactive
from textual.widget import Widget

from .. import styles
from ..renderables.record import LogRecord

PANEL_SIZE = 10


class Records(Widget):

    height: Reactive[int | None] = Reactive(None)

    def __init__(self, height: int | None = None):
        super().__init__()
        self.height = height
        self.records = [
            LogRecord(level=logging.INFO,
                      msg="The log messages will be displayed here as a list or table.")
        ]

    async def on_mount(self) -> None:
        # self.layout_size = PANEL_SIZE
        # self.layout_fraction = 1
        ...

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

    def update(self, records: List[LogRecord]):
        self.records.extend(records)
        # self.height = max(len(self.records), PANEL_SIZE)

    def _generate_renderable(self) -> ConsoleRenderable:
        text = Text(no_wrap=True)
        [
            text.append(record.__rich__()).append("\n")
            for record in self.records
            if self.app.levels.is_on(record.level)
        ]
        return text
