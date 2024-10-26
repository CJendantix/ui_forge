import curses
from curses import panel as cpanel
from typing import Callable
from .common import IndexedDict, DefaultKeymaps

# Classes are the closest thing a Rust programmer can get to enums in Python :'(


class Actions:
    Pass = 0
    Scroll_Down = 1
    Scroll_Up = 2
    Action = 3


def display_dict(
    pad: curses.window,
    dictionary: IndexedDict,
    selected_line: int,
    item_display: Callable[[tuple[str, dict], bool], tuple[str, int]],
):
    for line, (key, value) in enumerate(dictionary.items()):
        selected = (line == selected_line)

        display, attribute = item_display((key, value), selected)

        pad.addstr(line, 0, display, attribute)
        pad.addstr(line, len(display), " " * (pad.getmaxyx()[1] - len(display) - 1))


def scroll_down(
    current_line: int,
    pad_pos: int,
    max_scroll: int,
    window_bottom: int,
    offset: int = 2,
) -> tuple[int, int]:
    if current_line >= max_scroll - 1:
        return (current_line, pad_pos)

    current_line += 1
    if (
        current_line - pad_pos + offset >= window_bottom
        and current_line + offset < max_scroll
    ):
        pad_pos += 1

    return (current_line, pad_pos)


def scroll_up(current_line: int, pad_pos: int, offset: int = 2) -> tuple[int, int]:
    if current_line <= 0:
        return (current_line, pad_pos)

    if current_line - offset == pad_pos and current_line > offset:
        pad_pos -= 1
    current_line -= 1

    return (current_line, pad_pos)


def process_command(command: int, keymap: dict = DefaultKeymaps.View) -> int:
    if command in keymap["down"]:
        return Actions.Scroll_Down
    elif command in keymap["up"]:
        return Actions.Scroll_Up
    elif command in keymap["action"]:
        return Actions.Action
    else:
        return Actions.Pass


def dict_select(
    base_win: curses.window,
    dictionary: IndexedDict,
    item_display: Callable[[tuple[str, dict], bool], tuple[str, int]],
) -> tuple[str, dict]:
    base_dimensions = base_win.getmaxyx()
    top_left = base_win.getbegyx()
    bottom_right = (
        base_dimensions[0] + top_left[0],
        base_dimensions[1] + top_left[1],
    )

    pad = curses.newpad(len(dictionary), base_dimensions[1])
    pad.keypad(True)
    panel = cpanel.new_panel(pad)

    selected_line = 0
    pad_pos = 0

    while True:
        display_dict(pad, dictionary, selected_line, item_display)
        pad.refresh(pad_pos, 0, *top_left, *bottom_right)

        action = process_command(pad.getch())

        if action == Actions.Pass:
            continue
        elif action == Actions.Scroll_Up:
            selected_line, pad_pos = scroll_up(selected_line, pad_pos)
        elif action == Actions.Scroll_Down:
            selected_line, pad_pos = scroll_down(
                selected_line, pad_pos, len(dictionary), bottom_right[0] + 1
            )
        elif action == Actions.Action:
            panel.hide()
            return dictionary.from_index(selected_line)
