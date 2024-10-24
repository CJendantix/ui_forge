import curses
from curses import panel as cpanel
from common import IndexedDict
import collections
import copy
from view import dict_select

def list_get_or_none(list_input: list, i: int):
    try:
        return list_input[i]
    except IndexError:
        return None

def action_run_function(item: dict):
    item["function"](*item["args"], **item["kwargs"])

def action_select(item: (str, dict), dictionary: dict, base_panel: cpanel.panel, top_left: (int, int)):
    options = collections.OrderedDict()
    for option in item[1]["options"]:
        options[option[0]] = {
            "functionality": "option",
            "always_show_description": True
        }
        if description := list_get_or_none(option, 1):
            options[option[0]]["description"] = description
    dictionary[item[0]]["value"] = dict_select(base_panel, top_left, IndexedDict(options))[0]

def dict_ui(window, top_left: (int, int), original_dictionary: collections.OrderedDict) -> dict:
    base_panel = cpanel.new_panel(window)
    new_dictionary = copy.deepcopy(original_dictionary)
    
    while True:
        item = dict_select(base_panel, top_left, IndexedDict(new_dictionary))
        functionality = item[1]["functionality"]
        
        if functionality == "run_function":
            action_run_function(item[1])
        elif functionality == "select":
            action_select(item, new_dictionary, base_panel, top_left)
        else:
            window.addstr(0,0,str(item))
    
    base_panel.hide()
    return new_dictionary

def _tests(stdscr):
    import test_utils
    
    
    testing_dict = collections.OrderedDict({
        "run function test": {
            "functionality": "run_function",
            "description": "description",
            "always_show_description": True,
            "function": test_utils.testing_function,
            "args": ("a_working", "b_working"),
            "kwargs": {
                "c": "c_working",
                "d": "d_working"
            }
        },
        "edit test": {
            "functionality": "edit",
            "description": "description",
            "value": "value"
        },
        "selection test": {
            "functionality": "select",
            "description": "description",
            "value": "a",
            "options": [
                ["a", "description"],
                ["b"],
                ["c", "description"]
            ]
        }
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
    
    top_left = (0,0)
    dict_ui_win = curses.newwin(curses.LINES - top_left[0], curses.COLS - top_left[1], *top_left)
    dict_ui(dict_ui_win, top_left, testing_dict)
    
    stdscr.getch()
    
if __name__ == '__main__':
    curses.wrapper(_tests)