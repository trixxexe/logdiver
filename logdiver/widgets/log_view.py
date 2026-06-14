from textual.widgets import RichLog
from rich.text import Text
from logdiver.parser import parse_line


class LogView(RichLog):
    can_focus = False
    wrap = False

    def load_lines(self, lines: list[str]) -> None:
        self.clear()
        self._error_indices = []
        for i, line in enumerate(lines):
            if "ERROR" in line or "CRITICAL" in line:
                self._error_indices.append(i)
            self.write(parse_line(i + 1, line))

    def get_error_indices(self) -> list[int]:
        return self._error_indices
