from rich.console import RenderableType
from rich.panel import Panel

from textualog import styles
from textualog.renderables.namespace_tree import NamespaceTree


class Namespaces(NamespaceTree):
    def __init__(self, name=None, data: dict = None):
        self.tree: dict = data
        super().__init__(name=name, data=data)

    def render(self) -> RenderableType:
        panel = Panel(
            super().render(),
            title="[bold]Namespaces[/]",
            border_style=styles.BORDER,
            box=styles.BOX,
            title_align="left",
            padding=0,
        )
        return panel
