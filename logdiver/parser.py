"""Log line parsing and color detection."""

from rich.text import Text


def parse_line(line_number: int, raw_text: str) -> Text:
    text = Text()
    text.append(f"{line_number:>6} | ", style="dim")

    line = raw_text.rstrip("\n")

    if "ERROR" in line or "CRITICAL" in line:
        text.append(line, style="bold red")
    elif "WARNING" in line or "WARN" in line:
        text.append(line, style="yellow")
    elif "INFO" in line:
        text.append(line, style="cyan")
    elif "DEBUG" in line:
        text.append(line, style="dim white")
    else:
        text.append(line, style="white")

    return text
