from textual.widgets import Footer


class Footer(Footer):

    def on_mount(self) -> None:
        self.layout_size = 1

    def render(self):
        return super().render()
