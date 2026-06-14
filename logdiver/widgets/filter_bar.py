from textual.widget import Widget
from textual.widgets import Input
from textual.reactive import Reactive
from textual.message import Message


class FilterBar(Widget):

    DEFAULT_CSS = """
    FilterBar {
        height: 1;
        dock: bottom;
        background: $surface;
        padding: 0 1;
        display: none;
    }
    FilterBar.visible {
        display: block;
    }
    FilterBar Input {
        width: 100%;
    }
    """

    class Submitted(Message):
        def __init__(self, value: str) -> None:
            self.value = value
            super().__init__()

    class Cleared(Message):
        pass

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.filter_input = Input(
            placeholder="Type regex filter... (Enter to apply, Escape to clear)",
            id="filter-input",
        )

    def compose(self):
        yield self.filter_input

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.post_message(self.Submitted(event.value))

    def on_key(self, event) -> None:
        if event.key == "escape":
            self.post_message(self.Cleared())
