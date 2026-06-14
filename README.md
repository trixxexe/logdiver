# logdiver

[![PyPI version](https://badge.fury.io/py/logdiver.svg)](https://pypi.org/project/logdiver/)
[![Python](https://img.shields.io/pypi/pyversions/logdiver)](https://pypi.org/project/logdiver/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/YOUR_USERNAME/logdiver/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/logdiver/actions)

A beautiful, keyboard-driven TUI log file explorer for the terminal.

Built with [Textual](https://github.com/Textualize/textual) and [Rich](https://github.com/Textualize/rich).

```
     1 | 2024-01-15 10:00:00 INFO  Application started
     2 | 2024-01-15 10:00:01 DEBUG Initializing modules
     3 | 2024-01-15 10:00:02 WARN  High memory usage detected
     4 | 2024-01-15 10:00:03 ERROR Connection failed to database
     5 | 2024-01-15 10:00:04 INFO  Retrying connection...
     6 | 2024-01-15 10:00:05 CRIT  Fatal error in main process
     7 | 2024-01-15 10:00:06 INFO  Application shutting down
```

## Installation

```bash
pip install logdiver
```

## Usage

```bash
logdiver /var/log/syslog
logdiver /path/to/your/app.log
```

If no file is given, a file picker is shown.

## Keybindings

| Key | Action |
|-----|--------|
| `q` | Quit |
| `r` | Reload file |
| `t` | Toggle live tail mode |
| `w` | Toggle line wrap |
| `e` | Jump to next error |
| `E` | Jump to previous error |
| `g` | Jump to top |
| `G` | Jump to bottom |
| `/` | Open filter bar |
| `Esc` | Clear filter / close filter bar |

## Features

- **Color-coded log levels** -- ERROR/CRITICAL in red, WARNING in yellow, INFO in cyan, DEBUG in dim white
- **Live tail mode** -- Auto-scrolls as new lines are appended to the file
- **Regex filtering** -- Filter lines by pattern with case-insensitive matching
- **Error navigation** -- Jump between ERROR and CRITICAL lines with `e`/`E`
- **Line wrap toggle** -- Switch between horizontal scroll and wrapped lines
- **Binary file detection** -- Rejects binary files with a clear error message
- **Large file support** -- Handles large log files efficiently
- **File picker** -- Browse the filesystem if no file is given on launch

## Requirements

- Python 3.10+
- [Textual](https://pypi.org/project/textual/) >= 0.50.0
- [Rich](https://pypi.org/project/rich/) >= 13.0.0

## License

MIT License. See [LICENSE](LICENSE) for details.
