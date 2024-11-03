from dataclasses import dataclass, field
from typing import Callable, Tuple, Dict, Any, OrderedDict


@dataclass(kw_only=True)
class Item:
    """An Item with no functionality besides possible arguments (exit_after_action, for example)

    Args:
        description (str): The description of the item. Defaults to ""
        always_show_description (bool): Whether or not to always show the description. Defaults to False
        exit_after_action (bool): Whether or not to exit after the user chooses this item. Defaults to False
    """

    description: str = ""
    always_show_description: bool = False
    exit_after_action: bool = False


@dataclass(kw_only=True)
class RunFunctionItem(Item):
    """An item that runs an input function when pressed

    Args:
        function (Callable[..., None]): The function to run. Cannot have a return value.
        args (Tuple[Any, ...]): The arguments to pass the function. Defaults to ()
        kwargs (Dict[str, Any]): The keyword arguments to pass to the function. Defaults to {}
    """

    function: Callable[..., None]
    args: Tuple = ()
    kwargs: Dict[str, Any] = field(default_factory=dict)


@dataclass(kw_only=True)
class EditItem(Item):
    """An item that opens an editor for the value

    Args:
        value (str): The current value. Will be overwritten
        validator (Callable[[str], bool]): A function that takes the full string the user is attempting to input and returns whether or not to accept the value. Defaults to a function that always returns True
        header (str): A header above what the user is editing. Defaults to ""
        display_value (bool): Whether or not to display the value in the main screen. Defaults to True
    """

    value: str
    validator: Callable[[str], bool] = lambda _: True
    header: str = ""
    display_value: bool = True


@dataclass(kw_only=True)
class OptionItem(Item):
    """Item representing an option in a selection menu.

    Args:
        value (Any): The option's value.
        displayed_value (str): String to display for the option; defaults to "".
    """

    value: Any
    displayed_value: str = ""


@dataclass(kw_only=True)
class SelectionItem(Item):
    """Item that allows selection from multiple options.

    Args:
        value (Any): Selected value.
        options (OrderedDict[str, OptionItem]): Available options.
        display_value (bool): Show value on main screen; defaults to True.
        start_line (int): Initial selected line; defaults to 0.
        start_scroll (int): Initial scroll position; defaults to 0.
    """

    value: Any
    options: OrderedDict[str, OptionItem]
    display_value: bool = True
    start_line: int = 0
    start_scroll: int = 0


@dataclass(kw_only=True)
class SubMenuItem(Item):
    """Item that represents a submenu.

    Args:
        menu (OrderedDict[str, Item]): Submenu items.
    """

    menu: OrderedDict[str, Item]
