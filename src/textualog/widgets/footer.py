from rich.align import Align
from rich.columns import Columns
from rich.padding import Padding
from textual.reactive import Reactive
from textual.widgets import Footer


class Footer(Footer):

    log_size = Reactive(0)
    log_offset = Reactive(0)

    def on_mount(self) -> None:
        self.layout_size = 1

    def render(self) -> Columns:
        log_size_text = Align.right(
            Padding(
                f"at {self.log_offset} in [bold]{self.log_size}[/] lines", pad=(0, 1, 0, 1),
                style="white on dark_green",
                expand=False,
            )
        )

        return Columns([super().render(), log_size_text], expand=True)
