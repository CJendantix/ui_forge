import curses
from typing import Callable
from .common import IndexedDict
from .selector import dict_select


def run_function(item: dict):
    item["function"](*item["args"], **item["kwargs"])


def select(
    base_win: curses.window,
    options: dict,
    item_display: Callable[[tuple[str, dict], bool], str],
) -> str:
    base_win.clear()
    base_win.refresh()
    return dict_select(base_win, IndexedDict(options), item_display)[0]
