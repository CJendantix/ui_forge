import collections
import curses
from typing import Optional


class IndexedDict(collections.OrderedDict):
    def from_index(self, index: int) -> tuple:
        return list(self.items())[index]


class SpecialKeys:
    Enter = 10


class DefaultKeymaps:
    """Use this as a base to create your own keymap for the selector"""

    View = {
        "up": [curses.KEY_UP],
        "down": [curses.KEY_DOWN],
        "action": [SpecialKeys.Enter],
    }


def get_key_from_value(value: str, dictionary: dict) -> Optional[str]:
    for key, kvalue in dictionary.items():
        if str(value) == str(kvalue["value"]):
            return key


def default_item_display(item: tuple[str, dict], selected: bool) -> tuple[str, int]:
    """Use this as a base to create your own item displays.
    Args:
        item (tuple[str, dict]): The item being displayed, in item format.
        selected (bool): Whether or not this is the currently selected item.
    Returns:
        tuple[str, int]: A tuple containing the display string and the curses attribute to use.
    """
    key = item[0]
    data = item[1]
    functionality = data.get("functionality")

    item_display = ""
    attribute = curses.A_NORMAL

    if functionality == "run_function":
        item_display = f"{key}"
    elif functionality == "edit":
        if data.get("display_value") is False:
            item_display = f"{key}"
        else:
            item_display = f"{key}: {data["value"]}"
    elif functionality == "select":
        if data.get("display_value") is False:
            item_display = f"{key}"
        elif displayed_value := data["options"][
            get_key_from_value(data["value"], data["options"])
        ].get("displayed_value"):
            item_display = f"{key}: {displayed_value}"
        else:
            item_display = f"{key}: {data["value"]}"
    elif functionality == "sub_menu":
        item_display = f"{key}: ..."
    else:
        item_display = f"{key}"

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
