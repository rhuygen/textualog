from rich.panel import Panel
from textual.widget import Widget

from textualog import styles
from textualog.emojis import INFO
from textualog.renderables.shortcuts import Shortcuts


class Help(Widget):
    def render(self) -> Panel:
        return Panel(
            Shortcuts(),
            title=f"{INFO} [bold]help[/]",
            border_style=styles.BORDER_FOCUSED,
            box=styles.BOX,
            title_align="left",
            padding=0,
        )
