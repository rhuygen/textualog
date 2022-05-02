from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Union

import rich
from rich.console import RenderableType
from rich.text import Text
from textual import events
from textual._types import MessageTarget
from textual.message import Message
from textual.reactive import Reactive
from textual.widgets import NodeID
from textual.widgets import TreeClick
from textual.widgets import TreeControl
from textual.widgets import TreeNode


@dataclass
class NamespaceEntry:
    name: dict
    is_parent: bool

    def __str__(self):
        return f"{type(self.name)=}, {self.name=}, {self.is_parent=}"


@rich.repr.auto
class EntryClick(Message, bubble=True):
    def __init__(self, sender: MessageTarget, key: Union[dict, str]) -> None:
        self.key = key
        super().__init__(sender)


class NamespaceTree(TreeControl[NamespaceEntry]):
    def __init__(self, data: dict = None, name: str = None):
        label = "log"
        data = NamespaceEntry(data, True)
        super().__init__(label, name=name, data=data)
        self.root.tree.guide_style = "black"

    has_focus: Reactive[bool] = Reactive(False)
    mouse_over: Reactive[bool] = Reactive(False)
    style: Reactive[str] = Reactive("")
    height: Reactive[int | None] = Reactive(None)

    def on_focus(self) -> None:
        self.has_focus = True

    def on_blur(self) -> None:
        self.has_focus = False

    async def watch_hover_node(self, hover_node: NodeID) -> None:
        for node in self.nodes.values():
            node.tree.guide_style = (
                "bold not dim red" if node.id == hover_node else "black"
            )
        self.refresh(layout=True)

    def render_node(self, node: TreeNode[NamespaceEntry]) -> RenderableType:
        return self.render_tree_label(
            node,
            node.data.is_parent,
            node.expanded,
            node.is_cursor,
            node.id == self.hover_node,
            self.has_focus,
        )

    @lru_cache(maxsize=1024 * 32)
    def render_tree_label(
        self,
        node: TreeNode[NamespaceEntry],
        is_parent: bool,
        expanded: bool,
        is_cursor: bool,
        is_hover: bool,
        has_focus: bool,
    ) -> RenderableType:
        meta = {
            "@click": f"click_label({node.id})",
            "tree_node": node.id,
            "cursor": node.is_cursor,
        }
        label = Text(node.label) if isinstance(node.label, str) else node.label
        if is_hover:
            label.stylize("underline")
        if is_parent:
            label.stylize("bold magenta")
            icon = "▼︎" if expanded else "▶︎"
        else:
            label.stylize("bright_green")
            icon = ""
            label.highlight_regex(r"\..*$", "green")

        if label.plain.startswith("."):
            label.stylize("dim")

        if is_cursor and has_focus:
            label.stylize("reverse")

        icon_label = Text(f"{icon} ", no_wrap=True, overflow="ellipsis") + label
        icon_label.apply_meta(meta)
        return icon_label

    async def on_mount(self, event: events.Mount) -> None:
        await self.load_tree(self.root)

    async def load_tree(self, node: TreeNode[NamespaceEntry]):
        try:
            keys = sorted(node.data.name.keys())
        except AttributeError:
            keys = []
        for key in keys:
            is_dir = isinstance(node.data.name[key], dict)
            await node.add(key, NamespaceEntry(node.data.name[key], is_dir))
        node.loaded = True
        await node.expand()
        self.refresh(layout=True)

    async def handle_tree_click(self, message: TreeClick[NamespaceEntry]) -> None:
        namespace_entry = message.node.data
        if not namespace_entry.is_parent:
            await self.emit(EntryClick(self, namespace_entry.name))
        else:
            await self.emit(EntryClick(self, namespace_entry.name))
            if not message.node.loaded:
                await self.load_tree(message.node)
                await message.node.expand()
            else:
                await message.node.toggle()
