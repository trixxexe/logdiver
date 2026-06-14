"""Main Textual App class for logdiver."""

import re
import os
from pathlib import Path
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, DirectoryTree, Static, Input
from textual.containers import Container
from textual import on

from logdiver.widgets.header import HeaderBar
from logdiver.widgets.log_view import LogView
from logdiver.widgets.filter_bar import FilterBar


class LogDiverApp(App):
    """Main application for logdiver."""

    TITLE = "logdiver"
    SUB_TITLE = "Log file explorer"

    CSS = """
    Screen {
        layers: base overlay;
    }
    #main-container {
        height: 1fr;
    }
    LogView {
        height: 1fr;
        border: none;
    }
    #file-picker {
        height: 1fr;
    }
    #error-panel {
        height: auto;
        padding: 1 2;
        background: $error;
        color: $text;
    }
    FilterBar {
        dock: bottom;
        height: 1;
        display: none;
    }
    FilterBar.visible {
        display: block;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "reload", "Reload"),
        Binding("t", "toggle_live", "Live"),
        Binding("w", "toggle_wrap", "Wrap"),
        Binding("e", "next_error", "Next Error"),
        Binding("shift+e", "prev_error", "Prev Error"),
        Binding("g", "top", "Top"),
        Binding("shift+g", "bottom", "Bottom"),
        Binding("slash", "open_filter", "Filter"),
    ]

    def __init__(self, filepath: str | None = None) -> None:
        super().__init__()
        self._initial_filepath = filepath
        self._all_lines: list[str] = []
        self._filtered_lines: list[str] = []
        self._error_idx: list[int] = []
        self._error_cursor: int = -1
        self._live_mode: bool = False
        self._filter_active: bool = False
        self._last_mtime: float = 0
        self._last_line_count: int = 0
        self._filepath: str = ""

    def compose(self) -> ComposeResult:
        yield HeaderBar(id="header")
        yield Static("", id="error-panel")
        with Container(id="main-container"):
            yield LogView(id="log-view", wrap=False, highlight=False, markup=False)
            yield DirectoryTree("/", id="file-picker")
        yield FilterBar(id="filter-bar")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "logdiver"
        if self._initial_filepath:
            self._filepath = self._initial_filepath
            self.query_one("#file-picker").display = False
            self.query_one("#error-panel").display = False
            self._load_file(self._initial_filepath)
        else:
            self.query_one("#log-view").display = False
        self.set_interval(0.5, self._check_tail)

    def _load_file(self, filepath: str) -> None:
        path = Path(filepath)
        error_panel = self.query_one("#error-panel", Static)

        if not path.exists():
            error_panel.display = True
            error_panel.update(f"[bold red]Error:[/bold red] File not found: {filepath}")
            return

        if not os.access(filepath, os.R_OK):
            error_panel.display = True
            error_panel.update(f"[bold red]Error:[/bold red] Permission denied: {filepath}")
            return

        if not path.is_file():
            error_panel.display = True
            error_panel.update(f"[bold red]Error:[/bold red] Not a file: {filepath}")
            return

        try:
            with open(filepath, "rb") as f:
                chunk = f.read(8192)
                if b"\x00" in chunk:
                    error_panel.display = True
                    error_panel.update(
                        f"[bold red]Error:[/bold red] Binary file detected: {filepath}"
                    )
                    return
        except OSError as e:
            error_panel.display = True
            error_panel.update(f"[bold red]Error:[/bold red] {e}")
            return

        error_panel.display = False

        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                self._all_lines = [line.rstrip("\n\r") for line in f]
            self._last_mtime = path.stat().st_mtime
            self._last_line_count = len(self._all_lines)
        except Exception as e:
            error_panel.display = True
            error_panel.update(f"[bold red]Error:[/bold red] {e}")
            return

        self._filepath = filepath
        self._apply_lines(self._all_lines)

        header = self.query_one("#header", HeaderBar)
        header.filename = path.name
        header.file_size = self._format_size(path.stat().st_size)
        header.line_count = len(self._all_lines)

        log_view = self.query_one("#log-view", LogView)
        log_view.scroll_end(animate=False)

    def _format_size(self, size: int) -> str:
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.1f} {unit}" if unit != "B" else f"{size} B"
            size /= 1024
        return f"{size:.1f} TB"

    def _apply_lines(self, lines: list[str]) -> None:
        log_view = self.query_one("#log-view", LogView)
        log_view.load_lines(lines)
        self._error_idx = log_view.get_error_indices()
        self._error_cursor = -1

    def _check_tail(self) -> None:
        if not self._live_mode or not self._filepath:
            return
        try:
            path = Path(self._filepath)
            if not path.exists():
                self.notify("File deleted!", severity="warning")
                self._live_mode = False
                self.query_one("#header", HeaderBar).live_mode = False
                return
            mtime = path.stat().st_mtime
            if mtime != self._last_mtime:
                self._last_mtime = mtime
                with open(self._filepath, "r", encoding="utf-8", errors="replace") as f:
                    self._all_lines = [line.rstrip("\n\r") for line in f]
                self._apply_lines(self._all_lines)
                header = self.query_one("#header", HeaderBar)
                header.line_count = len(self._all_lines)
                self.query_one("#log-view", LogView).scroll_end(animate=False)
        except FileNotFoundError:
            self.notify("File deleted!", severity="warning")
            self._live_mode = False

    @on(DirectoryTree.FileSelected)
    def on_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        filepath = str(event.path)
        self._load_file(filepath)
        self.query_one("#file-picker").display = False
        self.query_one("#log-view").display = True

    # --- ACTIONS ---

    def action_reload(self) -> None:
        if self._filepath:
            self._load_file(self._filepath)
            self.notify("Reloaded")

    def action_toggle_live(self) -> None:
        self._live_mode = not self._live_mode
        self.query_one("#header", HeaderBar).live_mode = self._live_mode
        self.notify(f"Live tail {'ON' if self._live_mode else 'OFF'}")

    def action_toggle_wrap(self) -> None:
        lv = self.query_one("#log-view", LogView)
        lv.wrap = not lv.wrap
        lines = self._filtered_lines if self._filter_active else self._all_lines
        self._apply_lines(lines)
        self.notify(f"Wrap {'ON' if lv.wrap else 'OFF'}")

    def action_next_error(self) -> None:
        if not self._error_idx:
            self.notify("No errors found")
            return
        self._error_cursor = (self._error_cursor + 1) % len(self._error_idx)
        self.query_one("#log-view", LogView).scroll_to(
            y=self._error_idx[self._error_cursor], animate=False
        )

    def action_prev_error(self) -> None:
        if not self._error_idx:
            self.notify("No errors found")
            return
        self._error_cursor = (self._error_cursor - 1) % len(self._error_idx)
        self.query_one("#log-view", LogView).scroll_to(
            y=self._error_idx[self._error_cursor], animate=False
        )

    def action_top(self) -> None:
        self.query_one("#log-view", LogView).scroll_home(animate=False)

    def action_bottom(self) -> None:
        self.query_one("#log-view", LogView).scroll_end(animate=False)

    def action_open_filter(self) -> None:
        fb = self.query_one("#filter-bar", FilterBar)
        fb.add_class("visible")
        fb.filter_input.focus()

    def on_filter_bar_submitted(self, event: FilterBar.Submitted) -> None:
        pattern = event.value.strip()
        if not pattern:
            self._clear_filter()
            return
        try:
            rx = re.compile(pattern, re.IGNORECASE)
        except re.error:
            self.notify("Invalid regex", severity="error")
            return
        self._filtered_lines = [l for l in self._all_lines if rx.search(l)]
        self._filter_active = True
        self._apply_lines(self._filtered_lines)
        self.query_one("#header", HeaderBar).filter_text = pattern
        self.query_one("#header", HeaderBar).match_count = len(self._filtered_lines)
        self.query_one("#filter-bar", FilterBar).remove_class("visible")
        self.notify(f"{len(self._filtered_lines)} matches")

    def on_filter_bar_cleared(self, event: FilterBar.Cleared) -> None:
        self._clear_filter()

    def _clear_filter(self) -> None:
        self._filter_active = False
        self._filtered_lines = []
        self._apply_lines(self._all_lines)
        self.query_one("#header", HeaderBar).filter_text = ""
        self.query_one("#header", HeaderBar).match_count = 0
        self.query_one("#filter-bar", FilterBar).remove_class("visible")
