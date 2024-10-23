import curses
from curses import panel as cpanel
from common import IndexedDict
import collections
from view import dict_view

def run_function(item: dict):
    item["function"](*item["args"], **item["kwargs"])

def dict_ui(window, top_left: (int, int), original_dictionary: collections.OrderedDict) -> dict:
    base_panel = cpanel.new_panel(window)
    
    item = dict_view(base_panel, top_left, IndexedDict(original_dictionary))
    functionality = item[1]["functionality"]
    
    if functionality == "run_function":
        run_function(item[1])
    else:
        window.addstr(0,0,str(item))
    
    
    base_panel.hide()
    return original_dictionary

def _tests(stdscr):
    import test_utils
    
    testing_dict = collections.OrderedDict({
        "run function test": {
            "functionality": "run_function",
            "function": test_utils.testing_function,
            "description": "description",
            "args": ("a_working", "b_working"),
            "kwargs": {
                "c": "c_working",
                "d": "d_working"
            }
        },
        "edit test": {
            "functionality": "edit",
            "value": "value",
            "description": "description"
        },
    })
    
    # testing_dict = {}
    # for i in range(0,101):
    #     testing_dict[str(i)] = {
    #         "functionality": "edit",
    #         "value": str(i),
    #         "description": "test",
    #         "always_show_description": True
    #     }
    
    curses.curs_set(0)
    if curses.has_colors():
        curses.use_default_colors()
    
    stdscr.addstr(0,0, "Hello Chat")
    stdscr.getch()
    
    top_left = (30,0)
    dict_ui_win = curses.newwin(curses.LINES - 30, curses.COLS, *top_left)
    dict_ui(dict_ui_win, top_left, testing_dict)
    stdscr.getch()
    
if __name__ == '__main__':
    curses.wrapper(_tests)