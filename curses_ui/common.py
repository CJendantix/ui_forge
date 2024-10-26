import collections
import curses


class IndexedDict(collections.OrderedDict):
    def from_index(self, index: int) -> tuple:
        return list(self.items())[index]


class SpecialKeys:
    Enter = 10


class DefaultKeymaps:
    View = {
        "up": [curses.KEY_UP],
        "down": [curses.KEY_DOWN],
        "action": [SpecialKeys.Enter],
    }


def default_item_display(item: tuple[str, dict], selected: bool) -> tuple[str, int]:
    key = item[0]
    data = item[1]
    functionality = data["functionality"]

    item_display = ""
    attribute = curses.A_NORMAL

    if (
        functionality == "run_function"
        or functionality == "option"
        or functionality == "quit"
    ):
        item_display = f"{key}"
    elif functionality == "edit" or functionality == "select":
        item_display = f"{key}: {data["value"]}"
    elif functionality == "sub_menu":
        item_display = f"{key}: ..."

    if selected:
        item_display = " > " + item_display
        attribute = curses.A_BOLD
    else:
        item_display = "  " + item_display

    if (description := data.get("description")) and (
        data.get("always_show_description") or selected
    ):
        item_display += f" - {description}"

    return (item_display, attribute)
