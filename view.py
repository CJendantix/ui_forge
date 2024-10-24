import curses
from curses import panel as cpanel
from common import IndexedDict, DefaultKeymaps

# Classes are the closest thing a Rust programmer can get to enums in Python :'(

class Actions():
    Pass = 0
    Scroll_Down = 1
    Scroll_Up = 2
    Action = 3

def generate_item_display(item: (str, dict), selected: bool = False) -> str:
    key, data = item
    functionality: str = data["functionality"]
    
    item_display = ""
    
    if selected:
        if functionality == "run_function" or functionality == "option":
            item_display = f" > {key}"
        elif functionality == "edit" or functionality == "select":
            item_display = f" > {key}: {data["value"]}"
        
        if description := data.get("description"):
            item_display += f" - {description}"
        
    else:
        if functionality == "run_function" or functionality == "option":
            item_display = f"  {key}"
        elif functionality == "edit" or functionality == "select":
            item_display = f"  {key}: {data["value"]}"
        
        if data.get("always_show_description"):
            if description := data.get("description"):
                item_display += f" - {description}"
            
    return item_display

def display_dict(panel: cpanel.panel, dictionary: IndexedDict, selected_line):
    pad = panel.window()
    for line, (key, value) in enumerate(dictionary.items()):
        selected = False
        attribute = curses.A_NORMAL
        if line == selected_line:
            selected = True
            attribute = curses.A_BOLD

        display = generate_item_display((key, value), selected)
        display = display + " "*(pad.getmaxyx()[1] - len(display) - 1)
    
        pad.addstr(line,0, display, attribute)

def scroll_down(current_line: int, pad_pos: int, max_scroll: int, window_bottom: int, offset: int = 2) -> (int, int):
    if current_line >= max_scroll - 1:
        return (current_line, pad_pos)
        
    current_line += 1
    if current_line - pad_pos + offset >= window_bottom and current_line + offset < max_scroll:
        pad_pos += 1
    
    return (current_line, pad_pos)

def scroll_up(current_line: int, pad_pos: int, offset: int = 2) -> (int, int):
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
        
def dict_select(base_panel: cpanel.panel, top_left: (int, int), dictionary: IndexedDict) -> (str, dict):
    base_dimensions = base_panel.window().getmaxyx()
    bottom_right = (base_dimensions[0] + top_left[0], base_dimensions[1] + top_left[1])
    
    pad = curses.newpad(len(dictionary), base_dimensions[1])
    pad.keypad(True)
    panel = cpanel.new_panel(pad)

    selected_line = 0
    pad_pos = 0
    
    while True:
        display_dict(panel, dictionary, selected_line)
        pad.refresh(pad_pos,0, *top_left, *bottom_right)
        
        action = process_command(pad.getch())
        
        if action == Actions.Pass:
            continue
        elif action == Actions.Scroll_Up:
            selected_line, pad_pos = scroll_up(selected_line, pad_pos)
        elif action == Actions.Scroll_Down:
            selected_line, pad_pos = scroll_down(selected_line, pad_pos, len(dictionary), bottom_right[0] + 1)
        elif action == Actions.Action:
            panel.hide()
            return dictionary.from_index(selected_line)