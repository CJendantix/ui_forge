import curses
from curses import panel as cpanel
from ui_forge import dict_ui, selection_ui, editor_ui
import re


def testing_function(selection_menu: dict, description: dict) -> None:
    keys = []
    for key in selection_menu.keys():
        keys.append(int(key))
    selection_menu[str(max(keys) + 1)] = {
        "functionality": "option",
        "description": {"value": "description"},
        "always_show_description": {"value": True},
    }
    description["value"] = f"adds an option to the selection tests ({len(selection_menu)})"


def testing_int_validator(value: str) -> bool:
    return re.match(r"[-+]?\d+$", value) is not None


def tests(stdscr: curses.window):
    from curses.textpad import rectangle
    
    selection_dict = {
        "1": {
            "functionality": "option",
            "description": {"value": "description"},
            "always_show_description": {"value": True},
        },
    }

    long_dict = {
        "exit": {"functionality": "none", "exit_after_action": {"value": True}},
    }

    for i in range(0, 101):
        long_dict[str(i)] = {
            "functionality": "edit",
            "description": {"value": f"long list value {i}"},
            "value": {"value": str(i)},
            "validator": {"value": testing_int_validator},
            "allowed_human_readable": {"value": "only integers allowed"},
        }
        
    function_description = {"value": "adds an option to the selection tests (1)"}

    testing_dict = {
        "quit": {"functionality": "none", "exit_after_action": {"value": True}},
        "run function test": {
            "functionality": "run_function",
            "description": function_description,
            "always_show_description": {"value": True},
            "function": {"value": testing_function},
            "args": {"value": [selection_dict, function_description]}
        },
        "edit test": {
            "functionality": "edit",
            "description": {"value": "description"},
            "value": {"value": "1"},
            "validator": {"value": testing_int_validator},
            "allowed_human_readable": {"value": "only integers allowed"},
        },
        "selection test": {
            "functionality": "select",
            "description": {"value": "description"},
            "value": {"value": "1"},
            "options": selection_dict,
        },
        "sub menu test": {"functionality": "sub_menu", "menu": long_dict},
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
    dict_ui(dict_ui_win, testing_dict)

    stdscr.addstr(
        0, 0, "This shows the selection widget, fullscreen. Press any key to continue"
    )
    stdscr.getch()
    top_left = (0, 0)
    selection_ui_win = curses.newwin(
        curses.LINES - top_left[0] - 1, curses.COLS - top_left[1], *top_left
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

    rectangle_win = curses.newwin(32, 71, 3, 0)
    rectangle_panel = cpanel.new_panel(rectangle_win)
    rectangle(rectangle_win, 4, 4, 30, 70)
    rectangle_win.refresh()
    top_left = (8, 6)
    dict_ui_win = curses.newwin(24, 63, *top_left)
    dict_ui(dict_ui_win, testing_dict)

    stdscr.addstr(2, 0, "This shows the selection widget." + " " * (curses.COLS - 32))
    stdscr.refresh()
    top_left = (8, 6)
    selection_ui_win = curses.newwin(24, 63, *top_left)
    selection_ui(selection_ui_win, selection_dict)

    stdscr.addstr(2, 0, "This shows the editor widget." + " " * (curses.COLS - 29))
    stdscr.refresh()
    top_left = (8, 6)
    editor_ui_win = curses.newwin(24, 63, *top_left)
    editor_ui(editor_ui_win, "test value", "a")

    rectangle_panel.hide()

    stdscr.getch()
    stdscr.clear()
    stdscr.addstr(0, 0, "Testing complete")
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(tests)
