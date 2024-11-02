import curses
from typing import Any, Optional, OrderedDict, Tuple
from . import items


class SpecialKeys:
    Enter = 10


class DefaultKeymaps:
    """Use this as a base to create your own keymap for the selector"""

    View = {
        "up": [curses.KEY_UP],
        "down": [curses.KEY_DOWN],
        "action": [SpecialKeys.Enter],
    }


def get_option_from_value(
    value: Any, dictionary: OrderedDict[str, items.OptionItem]
) -> Optional[items.OptionItem]:
    for option in dictionary.values():
        if str(value) == str(option.value):
            return option


def default_item_display[
    T: items.Item
](item: Tuple[str, T], selected: bool) -> Tuple[str, int]:
    """Use this as a base to create your own item displays.
    Args:
        item (tuple[str, dict]): The item being displayed, in item format.
        selected (bool): Whether or not this is the currently selected item.
    Returns:
        tuple[str, int]: A tuple containing the display string and the curses attribute to use.
    """
    key = item[0]
    data = item[1]

    item_display = ""
    attribute = curses.A_NORMAL

    if isinstance(data, items.RunFunctionItem):
        item_display = f"{key}"
    elif isinstance(data, items.EditItem):
        if not data.display_value:
            item_display = f"{key}"
        else:
            item_display = f"{key}: {data.value}"
    elif isinstance(data, items.SelectionItem):
        if not data.display_value:
            item_display = f"{key}"
        elif option := get_option_from_value(data.value, data.options):
            item_display = f"{key}: {option.displayed_value}"
        else:
            item_display = f"{key}: {data.value}"
    elif isinstance(data, items.SubMenuItem):
        item_display = f"{key}: ..."
    else:
        item_display = f"{key}"

    if selected:
        item_display = " > " + item_display
        attribute = curses.A_BOLD
    else:
        item_display = "  " + item_display

    if (description := data.description) and (data.always_show_description or selected):
        item_display += f" - {description}"

    return (item_display, attribute)
