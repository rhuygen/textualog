from rich.console import RenderableType
from rich.text import Text
from textual import events
from textual.app import App
from textual.keys import Keys
from textual.reactive import Reactive
from textual.widgets import Header
from textual.widgets import Footer
from textual.widgets import Placeholder
from textual.widgets import ScrollView

from textualog.renderables.namespace_tree import EntryClick
from textualog.widgets.footer import Footer
from textualog.widgets.help import Help
from textualog.widgets.levels import Levels
from textualog.widgets.namespaces import Namespaces


class TextualLog(App):

    show_help = Reactive(False)
    show_namespaces = Reactive(False)

    namespace_tree = {
        "egse": {
            "system": "system",
            "decorators": {"x": 1, "y": 2},
        }
    }

    async def on_mount(self, event: events.Mount) -> None:
        """
        Call after terminal goes in to application mode.
        """

        self.namespaces = Namespaces("Name space", self.namespace_tree)
        self.namespaces.layout_offset_x = -40

        self.help_widget = Help()
        self.help_widget.visible = False

        # Header / footer / dock
        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")
        await self.view.dock(self.namespaces, edge="left", size=40, z=1)
        await self.view.dock(self.help_widget, edge="right", size=40, z=1)
        grid = await self.view.dock_grid(edge="left", name="left")

        grid.add_column(size=30, name="left")
        grid.add_column(fraction=1, name="right", min_size=100)

        grid.add_row(fraction=1, name="top")
        grid.add_row(fraction=1, name="middle")
        grid.add_row(fraction=1, name="bottom")

        grid.add_areas(
            area1="left-start|right-end,top-start|middle-end",
            area2="left,bottom",
            area3="right,bottom",
        )

        self.levels = Levels()
        self.logs = ScrollView()

        grid.place(
            area1=Placeholder(name="area1"),  # self.logs,
            area2=self.levels,
            area3=Placeholder(name="area3"),
        )

    async def on_load(self) -> None:
        """
        Sent before going in to application mode.
        Bind keys here.
        """
        await self.bind("q", "quit", "Quit")
        await self.bind("?", "toggle_help", "Help")

    async def on_key(self, event) -> None:

        if event.key == "d":
            self.levels.debug_level = not self.levels.debug_level
        elif event.key == "i":
            self.levels.info_level = not self.levels.info_level
        elif event.key == "w":
            self.levels.warning_level = not self.levels.warning_level
        elif event.key == "e":
            self.levels.error_level = not self.levels.error_level
        elif event.key == "c":
            self.levels.critical_level = not self.levels.critical_level
        elif event.key == "n":
            self.show_namespaces = not self.show_namespaces
        elif event.key == Keys.Escape:
            self.show_help = False
            self.show_namespaces = False

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

        syntax: RenderableType = Text(f"Rendering the namespace: {message.key}")
        self.app.sub_title = "xxx"
        await self.logs.update(syntax)


TextualLog.run(title="Textual Log Viewer", log="textual.log")
