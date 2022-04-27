from rich.table import Table
from textual.keys import Keys

from textualog.unicodes import DOWN
from textualog.unicodes import LEFT
from textualog.unicodes import RIGHT
from textualog.unicodes import UP


class Shortcuts:
    shortcuts = {
        "navigation": {
            "help": "?",
            "navigate": f"{LEFT} {RIGHT} {UP} {DOWN}",
            "close dialog": Keys.Escape,
            "quit": f"{Keys.ControlC} or q",
            "Show Namespaces": "n",
        },
        "Toggle Logging Levels": {
            "DEBUG mode": "d",
            "INFO mode": "i",
            "WARNING mode": "w",
            "ERROR mode": "e",
            "CRITICAL mode": "c",
        },
    }

    def __str__(self) -> str:
        return str(self.shortcuts)

    def __rich__(self) -> Table:
        table = Table(box=None, expand=False, show_footer=False, show_header=False)
        table.add_column(style="magenta bold")
        table.add_column(style="yellow bold")
        for category, shortcuts in self.shortcuts.items():
            table.add_row(f"[blue bold]{category}[/]")
            for action, shortcut in shortcuts.items():
                table.add_row(f"{action}:", f"{shortcut}")
            table.add_row()

        return table
