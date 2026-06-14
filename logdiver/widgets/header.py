"""Header bar widget showing file stats and current filter."""

from textual.widget import Widget
from textual.reactive import Reactive
from rich.text import Text


class HeaderBar(Widget):
    """A header bar that displays file info and current filter."""

    DEFAULT_CSS = """
    HeaderBar {
        height: 1;
        dock: top;
        background: $accent;
        color: $text;
        padding: 0 1;
    }
    """

    filename: Reactive[str] = Reactive("")
    file_size: Reactive[str] = Reactive("")
    line_count: Reactive[int] = Reactive(0)
    filter_text: Reactive[str] = Reactive("")
    match_count: Reactive[int] = Reactive(0)
    live_mode: Reactive[bool] = Reactive(False)

    def render(self) -> Text:
        parts = []

        if self.filename:
            parts.append(Text(self.filename, style="bold"))

        if self.file_size:
            parts.append(Text(f" | {self.file_size}", style="dim"))

        if self.line_count > 0:
            parts.append(Text(f" | {self.line_count} lines", style="dim"))

        if self.live_mode:
            parts.append(Text(" [LIVE]", style="bold green"))

        if self.filter_text:
            parts.append(Text(f" | /{self.filter_text}", style="italic"))
            if self.match_count > 0:
                parts.append(Text(f" ({self.match_count} matches)", style="yellow"))

        result = Text()
        for part in parts:
            result.append_text(part)
        return result
