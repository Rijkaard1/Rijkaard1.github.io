"""Colored terminal output (ANSI colors).

Colors switch themselves off when output is piped or saved to a file, or when
the NO_COLOR environment variable is set, so logs stay plain text.
"""
import os
import re
import sys

RESET = "\x1b[0m"
BOLD = "\x1b[1m"
RED = "\x1b[91m"
YELLOW = "\x1b[93m"
GREEN = "\x1b[92m"
PURPLE = "\x1b[95m"


def _enable_windows_ansi():
    """Turn on ANSI color support in the Windows console (Windows 10 and later)."""
    if os.name != "nt":
        return True
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)  # standard output
        mode = ctypes.c_ulong()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        return bool(kernel32.SetConsoleMode(handle, mode.value | 0x0004))  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
    except Exception:
        return False


ENABLED = sys.stdout.isatty() and "NO_COLOR" not in os.environ and _enable_windows_ansi()

LEVEL_COLORS = {
    "WARNING": RED, "UNSAFE": RED, "HIGH": RED,
    "CAUTION": YELLOW, "WEAK": YELLOW, "NEW": YELLOW, "MODERATE": YELLOW,
    "OK": GREEN, "SAFE": GREEN, "LOW": GREEN,
}


def c(text, *codes):
    """Wrap text in color codes (returns it unchanged when colors are off)."""
    return "".join(codes) + text + RESET if ENABLED else text


def level_color(name):
    return LEVEL_COLORS.get(str(name).upper(), "")


_TAG = re.compile(r"^(\s*)\[(WARNING|CAUTION|SAFE|HIGH|NEW|LOW|MODERATE)\](.*)$")
_COUNT = re.compile(r"^(\s+)(WARNING|CAUTION)(.*?:\s*)(\d+)$")
_RATING = re.compile(r"^(\s+Safety rating\s*:\s*)(\w+)$")
_MENU_NUM = re.compile(r"^(\d+\))(\s.*)$")


def paint(line):
    """Color one line of output based on what it looks like."""
    if not ENABLED or "\x1b[" in line:
        return line
    s = line.strip()
    if s.startswith("---") and s.endswith("---"):
        return c(line, BOLD, GREEN)
    if re.match(r"^\s*===.*===", line):
        return c(line, BOLD, PURPLE)
    if s.startswith("!!"):
        return c(line, BOLD, YELLOW)
    m = _TAG.match(line)
    if m:
        return m.group(1) + c("[" + m.group(2) + "]", BOLD, level_color(m.group(2))) + m.group(3)
    m = _COUNT.match(line)
    if m and int(m.group(4)) > 0:
        col = level_color(m.group(2))
        return m.group(1) + c(m.group(2), col) + m.group(3) + c(m.group(4), BOLD, col)
    m = _RATING.match(line)
    if m:
        return m.group(1) + c(m.group(2), BOLD, level_color(m.group(2)))
    m = _MENU_NUM.match(line)
    if m:
        return c(m.group(1), PURPLE) + m.group(2)
    return line


def cprint(*args, sep=" ", end="\n", **kwargs):
    """print() that colors each line."""
    text = sep.join(str(a) for a in args)
    print("\n".join(paint(line) for line in text.split("\n")), end=end, **kwargs)
