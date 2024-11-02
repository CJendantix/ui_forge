import curses
from dataclasses import dataclass
from typing import Callable, List, OrderedDict, Tuple
from . import items
from enum import Enum


@dataclass
class Keymap:
    """Use this as a base to create your own keymap for the selector"""

    Up: List[int]
    Down: List[int]
    Action: List[int]


class Actions(Enum):
    Pass = 0
    Scroll_Down = 1
    Scroll_Up = 2
    Action = 3


def get_max_display_length[
    T: items.Item
](
    dictionary: dict, item_display: Callable[[Tuple[str, T], bool], Tuple[str, int]]
) -> int:
    displays = []
    for key, value in dictionary.items():
        displays.append(len(item_display((key, value), True)[0]))
    return max(displays)


def display_dict[
    T: items.Item
](
    pad: curses.window,
    dictionary: OrderedDict[str, T],
    selected_line: int,
    item_display: Callable[[Tuple[str, T], bool], Tuple[str, int]],
):
    for line, (key, value) in enumerate(dictionary.items()):
        selected = line == selected_line

        display, attribute = item_display((key, value), selected)

        pad.addstr(line, 0, display, attribute)
        pad.addstr(line, len(display), " " * (pad.getmaxyx()[1] - len(display) - 1))


def scroll_down(
    current_line: int,
    scroll: int,
    max_scroll: int,
    window_top: int,
    window_bottom: int,
    offset: int = 2,
) -> Tuple[int, int]:
    if current_line >= max_scroll - 1:
        return (current_line, scroll)

    current_line += 1
    current_screen_line = current_line + window_top - scroll
    if (
        current_screen_line + offset >= window_bottom
        and current_line + offset < max_scroll
    ):
        scroll += 1

    return (current_line, scroll)


def scroll_up(current_line: int, scroll: int, offset: int = 2) -> Tuple[int, int]:
    if current_line <= 0:
        return (current_line, scroll)

    if current_line - offset <= scroll and current_line > offset:
        scroll -= 1
    current_line -= 1

    return (current_line, scroll)


def process_command(
    command: int,
    Keymap: Keymap = Keymap([curses.KEY_UP], [curses.KEY_DOWN], [10]),
) -> Actions:
    if command in Keymap.Down:
        return Actions.Scroll_Down
    elif command in Keymap.Up:
        return Actions.Scroll_Up
    elif command in Keymap.Action:
        return Actions.Action
    else:
        return Actions.Pass


def dict_select[
    T: items.Item
](
    base_win: curses.window,
    dictionary: OrderedDict[str, T],
    item_display: Callable[[Tuple[str, items.Item], bool], Tuple[str, int]],
    start_line: int = 0,
    start_scroll: int = 0,
) -> Tuple[Tuple[str, T], Tuple[int, int]]:
    base_dimensions = base_win.getmaxyx()
    top_left = base_win.getbegyx()
    bottom_right = (
        base_dimensions[0] + top_left[0],
        base_dimensions[1] + top_left[1],
    )

    pad = curses.newpad(
        len(dictionary), get_max_display_length(dictionary, item_display) + 1
    )
    pad.keypad(True)

    selected_line = start_line
    scroll = start_scroll

    while True:
        display_dict(pad, dictionary, selected_line, item_display)
        pad.refresh(scroll, 0, *top_left, *bottom_right)

        action = process_command(pad.getch())

        if action == Actions.Pass:
            continue
        elif action == Actions.Scroll_Up:
            selected_line, scroll = scroll_up(selected_line, scroll)
        elif action == Actions.Scroll_Down:
            selected_line, scroll = scroll_down(
                selected_line,
                scroll,
                len(dictionary),
                top_left[0],
                bottom_right[0] + 1,
            )
        elif action == Actions.Action:
            pad.clear()
            pad.refresh(scroll, 0, *top_left, *bottom_right)
            return (list(dictionary.items())[selected_line], (selected_line, scroll))
