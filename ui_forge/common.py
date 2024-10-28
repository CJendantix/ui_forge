import collections
import curses


class IndexedDict(collections.OrderedDict):
    def from_index(self, index: int) -> tuple:
        return list(self.items())[index]


class SpecialKeys:
    Enter = 10


class DefaultKeymaps:
    """Use this as a base to create your own keymap for the selector
    """
    View = {
        "up": [curses.KEY_UP],
        "down": [curses.KEY_DOWN],
        "action": [SpecialKeys.Enter],
    }


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
    elif functionality == "edit" or functionality == "select":
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
