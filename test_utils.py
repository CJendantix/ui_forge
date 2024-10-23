from pathlib import Path
import curses
from curses import panel as cpanel
import json

def create_test_dict() -> dict:
    dictionary: dict = dict()
    for i in range(0,101):
        dictionary[i] = i
    return dictionary

def load_test_dict_file() -> dict:
    test_json_path: Path = Path('./tests.json')
    if not test_json_path.exists():
        test_dict = create_test_dict()
        test_json_path.write_text(json.dumps(test_dict, indent=2))
        return test_dict
    
    test_json = test_json_path.read_text()
    try:
        test_dict = json.loads(test_json)
    except Exception:
        test_dict = create_test_dict()
        test_json_path.write_text(json.dumps(test_dict, indent=2))
        return test_dict
    return test_dict

def save_test_dict_file(dictionary: dict) -> None:
    test_json_path: Path = Path('./tests.json')
    test_json = json.dumps(dictionary, indent=2)
    test_json_path.write_text(test_json)
    
def testing_function(a: str, b: str, c: str = "c", d: str = "d") -> None:
    string = f"{a} {b} {c} {d}"
    panel = cpanel.new_panel(curses.newwin(curses.LINES,len(string) + 1,0,0))
    window = panel.window()
    window.addstr(0,0, string)
    window.getch()
    panel.hide()