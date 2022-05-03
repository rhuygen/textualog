import argparse
import sys
from pathlib import Path

from textual import events
from textual.app import App
from textual.keys import Keys
from textual.reactive import Reactive
from textual.widgets import Header

from . import __version__
from .loader import KeyValueLoader
from .renderables.namespace_tree import EntryClick
from .widgets.footer import Footer
from .widgets.help import Help
from .widgets.levels import Levels
from .widgets.namespaces import Namespaces
from .widgets.recordinfo import RecordInfo
from .widgets.records import Records


class TextualLog(App):

    show_help = Reactive(False)
    show_namespaces = Reactive(False)

    # The namespace_tree is just for demonstration purposes. The namespace should be a
    # tree like structure with proper navigation and the possibility to add and remove nodes.

    namespace_tree = {
        "egse": {
            "system": "system",
            "decorators": {"x": 1, "y": 2},
        }
    }

    def __init__(self, filename: str = None, **kwargs):
        super().__init__(**kwargs)
        self.filename = filename
        self.cursor = 0
        self.loader = None

    async def on_mount(self, event: events.Mount) -> None:
        """
        Call after terminal goes in to application mode.
        """

        self.namespaces = Namespaces("Name space", self.namespace_tree)
        self.namespaces.layout_offset_x = -40

        self.help_widget = Help()
        self.help_widget.visible = False

        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")
        await self.view.dock(self.namespaces, edge="left", size=40, z=1)
        await self.view.dock(self.help_widget, edge="right", size=40, z=1)
        grid = await self.view.dock_grid(edge="left", name="left")

        grid.add_column(size=30, name="left")
        grid.add_column(fraction=1, name="right", min_size=100)

        grid.add_row(fraction=1, name="top")
        grid.add_row(fraction=1, name="middle")
        grid.add_row(size=7, name="bottom")

        grid.add_areas(
            area1="left-start|right-end,top-start|middle-end",
            area2="left,bottom",
            area3="right,bottom",
        )

        self.levels = Levels()
        self.records = Records()
        self.record_info = RecordInfo()

        grid.place(
            area1=self.records,
            area2=self.levels,
            area3=self.record_info,
        )

        if self.filename:
            self.loader = KeyValueLoader(self.filename)
            self.loader.load()
            self.loader.process(0, 500, None)

            # The height of the self.records view is not yet known, so we take a large enough number

            self.records.update(self.loader.get_records(0, 500, None))

    async def on_load(self) -> None:
        """
        Sent before going in to application mode. This method is called before on_mount().
        Bind keys here.
        """
        await self.bind("q", "quit", "Quit")
        await self.bind("?", "toggle_help", "Help")

    async def on_key(self, event) -> None:

        if self.loader is None:
            return

        # The height of the text area of the Records panel

        height = self.records.size.height - 2
        size = self.loader.size()

        self.app.sub_title = f"Key pressed: {event.key}"

        if event.key == "d":
            self.levels.debug_level = not self.levels.debug_level
            self.records.replace(self.loader.get_records(self.cursor, height, self.levels))
        elif event.key == "i":
            self.levels.info_level = not self.levels.info_level
            self.records.replace(self.loader.get_records(self.cursor, height, self.levels))
        elif event.key == "w":
            self.levels.warning_level = not self.levels.warning_level
            self.records.replace(self.loader.get_records(self.cursor, height, self.levels))
        elif event.key == "e":
            self.levels.error_level = not self.levels.error_level
            self.records.replace(self.loader.get_records(self.cursor, height, self.levels))
        elif event.key == "c":
            self.levels.critical_level = not self.levels.critical_level
            self.records.replace(self.loader.get_records(self.cursor, height, self.levels))
        elif event.key in "nN":
            self.show_namespaces = not self.show_namespaces
        elif event.key == Keys.Escape:
            self.show_help = False
            self.show_namespaces = False
        elif event.key == Keys.Down:
            self.cursor = min(size, self.cursor + 1)
            self.records.replace(self.loader.get_records(self.cursor, height, self.levels))
        elif event.key == Keys.Up:
            self.cursor = max(0, self.cursor - 1)
            self.records.replace(self.loader.get_records(self.cursor, height, self.levels))
        elif event.key == Keys.PageDown:
            self.cursor = min(size, self.cursor+(height-1))
            self.records.replace(self.loader.get_records(self.cursor, height, self.levels))
        elif event.key == Keys.PageUp:
            self.cursor = max(0, self.cursor-(height-1))
            self.records.replace(self.loader.get_records(self.cursor, height, self.levels))
        elif event.key == Keys.End:
            self.cursor = size - height
            self.records.replace(self.loader.get_records(self.cursor, height, self.levels))
        elif event.key == Keys.Home:
            self.cursor = 0
            self.records.replace(self.loader.get_records(self.cursor, height, self.levels))

        self.records.refresh(layout=True, repaint=True)

    async def watch_show_namespaces(self, show_namespaces: bool) -> None:
        """Called when show_namespaces changes."""
        self.namespaces.animate("layout_offset_x", 0 if show_namespaces else -40)

    async def watch_show_help(self, show_help: bool) -> None:
        """Called when show_help changes."""
        self.help_widget.visible = show_help

    async def action_toggle_help(self) -> None:
        """Called when bound help key is pressed."""
        self.show_help = not self.show_help

    async def handle_entry_click(self, message: EntryClick) -> None:
        """A message sent by the namespace tree when an entry is clicked."""

        self.app.sub_title = f"{message.key}"
        self.records.refresh(layout=True)


def main():
    from rich.traceback import install
    install(show_locals=False)

    parser = argparse.ArgumentParser(
        description="Textual Log Viewer, display, filter and search log files",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=_get_version_text(),
        help="display version information",
    )

    parser.add_argument(
        "--log",
        "-l",
        type=str,
        default=None,
        help="debug log file",
    )

    args = parser.parse_args()

    if args.log and not Path(args.log).exists():
        raise FileNotFoundError(f"No such file {args.log}")

    TextualLog.run(title="Textual Log Viewer", log=None, filename=args.log)


def _get_version_text():
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    return "\n".join(
        [
            f"textualog {__version__.__version__} [Python {python_version}]",
            "Copyright © 2022 Rik Huygen",
        ]
    )


if __name__ == "__main__":
    main()
