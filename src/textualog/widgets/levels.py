import logging

from rich.panel import Panel
from rich.table import Table
from textual.reactive import Reactive
from textual.widget import Widget

from textualog import styles
from textualog.emojis import CHECK
from textualog.emojis import UNCHECK

PANEL_SIZE = 5


class Levels(Widget):

    debug_level: Reactive = Reactive(True)
    info_level: Reactive = Reactive(True)
    warning_level: Reactive = Reactive(True)
    error_level: Reactive = Reactive(True)
    critical_level: Reactive = Reactive(True)

    async def on_mount(self) -> None:
        self.layout_size = PANEL_SIZE

    def render(self) -> Panel:
        table = Table(box=None, expand=False, show_header=False, show_edge=False)
        table.add_column()
        table.add_column()

        table.add_row(CHECK if self.debug_level else UNCHECK, "DEBUG")
        table.add_row(CHECK if self.info_level else UNCHECK, "INFO")
        table.add_row(CHECK if self.warning_level else UNCHECK, "WARNING")
        table.add_row(CHECK if self.error_level else UNCHECK, "ERROR")
        table.add_row(CHECK if self.critical_level else UNCHECK, "CRITICAL")

        panel = Panel(
            table,
            title="[bold]Levels[/]",
            border_style=styles.BORDER,
            box=styles.BOX,
            title_align="left",
            padding=0,
        )

        return panel

    def is_on(self, level: int):
        if level == logging.DEBUG:
            return self.debug_level
        elif level == logging.INFO:
            return self.info_level
        elif level == logging.WARNING:
            return self.warning_level
        elif level == logging.ERROR:
            return self.error_level
        elif level == logging.CRITICAL:
            return self.critical_level
        return False

    def __str__(self):
        return (
            f"DEBUG={'ON' if self.debug_level else 'OFF'}, "
            f"INFO={'ON' if self.info_level else 'OFF'}, "
            f"WARNING={'ON' if self.warning_level else 'OFF'}, "
            f"ERROR={'ON' if self.error_level else 'OFF'}, "
            f"CRITICAL={'ON' if self.critical_level else 'OFF'}"
        )
