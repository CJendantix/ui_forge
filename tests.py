import curses
from curses import panel as cpanel
from typing import Callable
from cursesui import dict_ui, selection_ui, editor_ui
import re


def testing_function(
    base_win: curses.window, a: str, b: str, c: str = "c", d: str = "d"
) -> None:
    string = f"{a} {b} {c} {d}"
    base_win.addstr(0, 0, string)
    base_win.getch()


def testing_int_validator(value: str) -> bool:
    return re.match(r"[-+]?\d+$", value) is not None


def tests(stdscr: curses.window):
    from curses.textpad import rectangle

    selection_dict = {
        "a": {
            "functionality": "option",
            "description": "description",
            "always_show_description": True,
        },
        "b": {
            "functionality": "option",
            "description": "description",
            "always_show_description": False,
        },
        "c": {
            "functionality": "option",
            "description": "description",
            "always_show_description": True,
        },
    }
    
    long_dict: dict[str, dict[str, str | Callable]] = {
        "quit": {"functionality": "quit"}
    }
    
    for i in range(0,101):
        long_dict[str(i)] = {
            "functionality": "edit",
            "description": f"long list value {i}",
            "value": str(i),
            "validator": testing_int_validator,
            "allowed_human_readable": "only integers allowed",
        }
    
    testing_dict = {
        "quit test": {"functionality": "quit"},
        "run function test": {
            "functionality": "run_function",
            "description": "description",
            "always_show_description": True,
            "function": testing_function,
            "args": [
                curses.newwin(len("a_working b_working c_working d_working"), 1, 0, 0),
                "a_working",
                "b_working",
            ],
            "kwargs": {"c": "c_working", "d": "d_working"},
        },
        "edit test": {
            "functionality": "edit",
            "description": "description",
            "value": "1",
            "validator": testing_int_validator,
            "allowed_human_readable": "only integers allowed",
        },
        "selection test": {
            "functionality": "select",
            "description": "description",
            "value": "a",
            "options": selection_dict,
        },
        "sub menu test": {
            "functionality": "sub_menu",
            "menu": long_dict
        },
    }

    curses.curs_set(0)
    if curses.has_colors():
        curses.use_default_colors()

    stdscr.addstr(0, 0, "UI Testing. Press any key to continue")
    stdscr.getch()

    stdscr.addstr(
        0, 0, "This shows the layered UI, fullscreen. Press any key to continue"
    )
    stdscr.getch()
    top_left = (0, 0)
    dict_ui_win = curses.newwin(
        curses.LINES - top_left[0] - 1, curses.COLS - top_left[1], *top_left
    )
    testing_dict["run function test"]["args"][
        0
    ] = dict_ui_win  # give function test bounds
    dict_ui(dict_ui_win, testing_dict)

    stdscr.addstr(
        0, 0, "This shows the selection widget, fullscreen. Press any key to continue"
    )
    stdscr.getch()
    top_left = (0, 0)
    selection_ui_win = curses.newwin(
        curses.LINES - top_left[0], curses.COLS - top_left[1], *top_left
    )
    selection_ui(selection_ui_win, selection_dict)

    stdscr.addstr(
        0, 0, "This shows the editor widget, fullscreen. Press any key to continue"
    )
    stdscr.getch()
    top_left = (0, 0)
    editor_ui_win = curses.newwin(
        curses.LINES - top_left[0], curses.COLS - top_left[1], *top_left
    )
    editor_ui(editor_ui_win, "test value", "Hello World")

    stdscr.addstr(
        0, 0, "The next few tests will not be fullscreen." + " " * (curses.COLS - 42)
    )
    stdscr.addstr(
        8,
        2,
        "This text will remain to show that the widgets do not interfere with text behind it.",
    )
    stdscr.addstr(2, 0, "This shows the layered UI. Press Any key to continue")
    stdscr.getch()

    rectangle_win = curses.newwin(32, 61, 3, 0)
    rectangle_panel = cpanel.new_panel(rectangle_win)
    rectangle(rectangle_win, 4, 4, 30, 60)
    rectangle_win.refresh()
    top_left = (8, 6)
    dict_ui_win = curses.newwin(24, 54, *top_left)
    testing_dict["run function test"]["args"][
        0
    ] = dict_ui_win  # give function test bounds    
    dict_ui(dict_ui_win, testing_dict)

    stdscr.addstr(2, 0, "This shows the selection widget." + " " * (curses.COLS - 32))
    stdscr.refresh()
    top_left = (8, 6)
    selection_ui_win = curses.newwin(21, 54, *top_left)
    selection_ui(selection_ui_win, selection_dict)

    stdscr.addstr(2, 0, "This shows the editor widget." + " " * (curses.COLS - 29))
    stdscr.refresh()
    top_left = (8, 6)
    editor_ui_win = curses.newwin(21, 54, *top_left)
    editor_ui(editor_ui_win, "test value", "a")

    rectangle_panel.hide()

    stdscr.getch()
    stdscr.clear()
    stdscr.addstr(0, 0, "Testing complete")
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(tests)
