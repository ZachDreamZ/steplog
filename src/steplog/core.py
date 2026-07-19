import contextlib
import dataclasses
import os
import sys
import threading
import time
from typing import Generator, Optional


_IS_WINDOWS = os.name == "nt"


def _enable_ansi():
    if _IS_WINDOWS:
        try:
            import ctypes

            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass


_enable_ansi()


_RESET = "\033[0m"
_BOLD = "\033[1m"
_DIM = "\033[2m"
_GREEN = "\033[92m"
_RED = "\033[91m"
_YELLOW = "\033[93m"
_CYAN = "\033[96m"
_WHITE = "\033[97m"
_GRAY = "\033[90m"


def _strip_ansi(text: str) -> str:
    import re
    return re.sub(r"\033\[[0-9;]*m", "", text)


def _fmt_time(seconds: float) -> str:
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    return f"{seconds:.1f}s"


@dataclasses.dataclass
class StepResult:
    label: str
    duration: float
    success: bool
    message: Optional[str] = None

    def __str__(self) -> str:
        icon = "✓" if self.success else "✗"
        color = _GREEN if self.success else _RED
        timing = _DIM + _fmt_time(self.duration) + _RESET
        msg = f" — {self.message}" if self.message else ""
        return f"{color}{icon}{_RESET} {self.label} {timing}{msg}"


@contextlib.contextmanager
def step(label: str) -> Generator[StepResult, None, None]:
    print(f"  {_BOLD}{label}{_RESET} ...", end="", flush=True)
    start = time.perf_counter()
    result = StepResult(label=label, duration=0.0, success=True)
    try:
        yield result
    except Exception as exc:
        duration = time.perf_counter() - start
        result.success = False
        result.duration = duration
        result.message = str(exc)
        print(f"\r  {_RED}✗{_RESET} {label} {_DIM}{_fmt_time(duration)}{_RESET} — {exc}")
        raise
    else:
        duration = time.perf_counter() - start
        result.duration = duration
        print(f"\r  {_GREEN}✓{_RESET} {label} {_DIM}{_fmt_time(duration)}{_RESET}")


class Spinner:
    _FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def __init__(self, message: str, delay: float = 0.1):
        self._message = message
        self._delay = delay
        self._thread: Optional[threading.Thread] = None
        self._stop = threading.Event()

    def _spin(self):
        i = 0
        while not self._stop.is_set():
            frame = self._FRAMES[i % len(self._FRAMES)]
            print(f"\r  {_CYAN}{frame}{_RESET} {self._message}", end="", flush=True)
            i += 1
            self._stop.wait(self._delay)

    def start(self):
        self._stop.clear()
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()

    def stop(self, success: bool = True):
        self._stop.set()
        if self._thread:
            self._thread.join()
        icon = f"{_GREEN}✓{_RESET}" if success else f"{_RED}✗{_RESET}"
        print(f"\r  {icon} {self._message}  ")


def spinner(message: str) -> Spinner:
    s = Spinner(message)
    s.start()
    return s


class Output:
    @staticmethod
    def info(text: str) -> None:
        print(f"  {_CYAN}ℹ{_RESET} {text}")

    @staticmethod
    def success(text: str) -> None:
        print(f"  {_GREEN}✓{_RESET} {text}")

    @staticmethod
    def warn(text: str) -> None:
        print(f"  {_YELLOW}⚠{_RESET} {text}")

    @staticmethod
    def error(text: str) -> None:
        print(f"  {_RED}✗{_RESET} {text}")

    @staticmethod
    def header(text: str) -> None:
        width = min(60, _get_terminal_width() - 2)
        print()
        print(f"  {_BOLD}{text}{_RESET}")
        print(f"  {_DIM}{'─' * width}{_RESET}")

    @staticmethod
    def subheader(text: str) -> None:
        print(f"  {_BOLD}{_GRAY}{text}{_RESET}")

    @staticmethod
    def table(headers: list[str], rows: list[list[str]]) -> None:
        if not rows:
            return
        col_widths = [
            max(len(_strip_ansi(str(h))), max(len(_strip_ansi(str(rows[i][j]))) for i in range(len(rows))))
            for j, h in enumerate(headers)
        ]
        sep = "  "
        hdr = sep.join(_BOLD + h.ljust(col_widths[i]) + _RESET for i, h in enumerate(headers))
        print(f"  {hdr}")
        print(f"  {_DIM}{'─' * (sum(col_widths) + len(sep) * (len(headers) - 1))}{_RESET}")
        for row in rows:
            line = sep.join(str(row[i]).ljust(col_widths[i]) for i in range(len(headers)))
            print(f"  {line}")
        print()

    @staticmethod
    def section(text: str) -> None:
        width = min(60, _get_terminal_width() - 2)
        print()
        print(f"  {_BOLD}{_WHITE}{text}{_RESET}")
        print(f"  {_DIM}{'═' * width}{_RESET}")
        print()

    @staticmethod
    def code(text: str) -> None:
        for line in text.split("\n"):
            print(f"  {_DIM}|{_RESET} {line}")

    @staticmethod
    def json(data: dict) -> None:
        import json
        for line in json.dumps(data, indent=2).split("\n"):
            print(f"  {_DIM}|{_RESET} {line}")

    @staticmethod
    def raw(text: str) -> None:
        print(f"  {text}")

    @staticmethod
    def divider() -> None:
        width = min(60, _get_terminal_width() - 2)
        print(f"  {_DIM}{'─' * width}{_RESET}")


def _get_terminal_width() -> int:
    try:
        import shutil
        return shutil.get_terminal_size().columns
    except Exception:
        return 80


output = Output()
