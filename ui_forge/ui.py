from collections import OrderedDict
import curses
from typing import Any, Callable, Optional, Tuple
from . import selector, actions, items


def get_option_from_value(
    value: Any, dictionary: OrderedDict[str, items.OptionItem]
) -> Optional[items.OptionItem]:
    for option in dictionary.values():
        if str(value) == str(option.value):
            return option


def default_item_display(
    item: Tuple[str, items.Item], selected: bool
) -> Tuple[str, int]:
    """Generates the display string and attributes for a menu item based on its type and selection status. Use as a base to create your own.

    Args:
        item (Tuple[str, items.Item]): Tuple containing the item key and the Item instance.
        selected (bool): Indicates if the item is currently selected.

    Returns:
        Tuple[str, int]: A tuple containing the formatted display string and its attributes.
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


def dict_ui(
    base_window: curses.window,
    ui: OrderedDict[str, items.Item],
    item_display: Callable[
        [Tuple[str, items.Item], bool], Tuple[str, int]
    ] = default_item_display,
    start_line: int = 0,
    start_scroll: int = 0,
):
    """Creates a user interface in a Curses window for interacting with an ordered dictionary of items.

    Args:
        base_window (curses.window): A Curses window with the widget's bounds
        ui (OrderedDict[str, items.Item]): An ordered dictionary of names and Items (any type)
        item_display (Callable[ [Tuple[str, items.Item], bool], Tuple[str, int] ], optional): The function that creates displays, override for a different style. Defaults to common.default_item_display.
        start_line (int, optional): The line that is selected by default. Defaults to 0.
        start_scroll (int, optional): The amount that is scrolled by default, weird behavior when value doesn't make sense compared to start_line. Defaults to 0.
    """
    while True:
        base_window.clear()
        base_window.refresh()

        item, (start_line, start_scroll) = selector.dict_select(
            base_window,
            OrderedDict(ui),
            item_display,
            start_line=start_line,
            start_scroll=start_scroll,
        )

        if isinstance(item[1], items.RunFunctionItem):
            actions.run_function(item[1])
        elif isinstance(item[1], items.SelectionItem):
            item[1].value = actions.select(
                base_window,
                item[1].options,
                item_display,
                start_line=item[1].start_line,
                start_scroll=item[1].start_scroll,
            )
        elif isinstance(item[1], items.EditItem):
            item[1].value = actions.edit(base_window, (item[0], item[1]))
        elif isinstance(item[1], items.SubMenuItem):
            dict_ui(base_window, item[1].menu)

        if item[1].exit_after_action:
            break

    base_window.clear()
    base_window.refresh()


def selection_ui(
    base_window: curses.window,
    options: OrderedDict[str, items.OptionItem],
    item_display: Callable[
        [Tuple[str, items.Item], bool], Tuple[str, int]
    ] = default_item_display,
    start_line: int = 0,
    start_scroll: int = 0,
) -> Any:
    """Displays a selection menu in a Curses window for choosing from an ordered dictionary of options.

    Args:
        base_window (curses.window): A Curses window with the widget's bounds
        options (OrderedDict[str, items.OptionItem]): An ordered dictionary of names and OptionItems
        item_display (Callable[ [Tuple[str, items.Item], bool], Tuple[str, int] ], optional): The function that creates displays, override for a different style. Defaults to common.default_item_display.
        start_line (int, optional): The line that is selected by default. Defaults to 0.
        start_pos (int, optional): The amount that is scrolled by default, weird behavior when value doesn't make sense compared to start_line. Defaults to 0.

    Returns:
        Any: The value of the selected OptionItem
    """
    value = actions.select(base_window, options, item_display, start_line, start_scroll)
    base_window.clear()
    base_window.refresh()
    return value


def editor_ui(
    base_window: curses.window,
    name: str,
    value: str = "",
    validator: Callable[[str], bool] = lambda _: True,
    allowed_human_readable: str = "",
) -> str:
    """Displays an editor interface for user input and returns the modified value.

    Args:
        base_window (curses.window): The Curses window for rendering the editor.
        name (str): The prompt or title for the editor.
        value (str, optional): Default value to display. defaults to "".
        validator (Callable[[str], bool], optional): Function to validate the input. Defaults to a function that always returns True.
        allowed_human_readable (str, optional): Explanation of allowed input values. Defaults to "".

    Returns:
        str: The user-modified value after validation.
    """
    value = actions.edit(
        base_window,
        (
            name,
            items.EditItem(
                value=value,
                validator=validator,
                allowed_human_readable=allowed_human_readable,
            ),
        ),
    )
    base_window.clear()
    base_window.refresh()
    return value
