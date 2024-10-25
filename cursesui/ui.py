import curses
from typing import Callable
from curses import panel as cpanel
from .selector import dict_select
from .common import IndexedDict, default_item_display
from .actions import run_function, select


def dict_ui(
    base_window: curses.window,
    dictionary: dict,
    item_display: Callable[[tuple[str, dict], bool], str] = default_item_display,
):
    base_panel = cpanel.new_panel(base_window)

    while True:
        item = dict_select(base_window, IndexedDict(dictionary), item_display)
        functionality = item[1]["functionality"]

        if functionality == "quit":
            break
        elif functionality == "run_function":
            run_function(item[1])
        elif functionality == "select":
            dictionary[item[0]]["value"] = select(
                base_window, item[1]["options"], item_display
            )

    base_panel.hide()


def selection_ui(
    base_window: curses.window,
    options: dict,
    item_display: Callable[[tuple[str, dict], bool], str] = default_item_display,
) -> str:
    base_panel = cpanel.new_panel(base_window)
    value = select(base_window, options, item_display)
    base_panel.hide()
    return value
