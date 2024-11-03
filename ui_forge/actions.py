import curses
from curses.textpad import Textbox
from typing import Any, Callable, OrderedDict, Tuple
from . import selector, items


def run_function(item: items.RunFunctionItem):
    item.function(*item.args, **item.kwargs)


def select(
    base_win: curses.window,
    options: OrderedDict[str, items.OptionItem],
    item_display: Callable[[Tuple[str, items.Item], bool], Tuple[str, int]],
    start_line: int = 0,
    start_scroll: int = 0,
) -> Any:
    base_win.clear()
    base_win.refresh()
    selection = selector.dict_select(
        base_win, options, item_display, start_line, start_scroll
    )[0]
    return selection[1].value


def edit(base_win: curses.window, item: items.EditItem) -> str:
    base_win.clear()
    base_win.refresh()

    curses.curs_set(1)

    dimensions = base_win.getmaxyx()
    top_right = base_win.getbegyx()

    edit_win = curses.newwin(*dimensions, *top_right)
    header = item.header
    
    textpad_win: curses.window
    
    if header:
        edit_win.addstr(0, 0, header)
        edit_win.addstr(2, 0, " > ")
        textpad_win = curses.newwin(
            1, dimensions[1] - 3, top_right[0] + 2, top_right[1] + 3
        )
    else:
        edit_win.addstr(0, 0, " > ")
        textpad_win = curses.newwin(
            1, dimensions[1] - 3, top_right[0], top_right[1] + 3
        )

    edit_win.refresh()
    textbox = Textbox(textpad_win, insert_mode=True)

    while True:
        textpad_win.clear()
        textpad_win.addstr(0, 0, item.value)
        textpad_win.refresh()

        value = textbox.edit().strip()
        validator = item.validator
        if not validator:
            validator = lambda x: True  # noqa: E731

        if validator(value):
            curses.curs_set(0)
            return value
