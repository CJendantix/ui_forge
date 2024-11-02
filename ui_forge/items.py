from dataclasses import dataclass, field
from typing import Callable, Tuple, Dict, Any, OrderedDict


@dataclass(kw_only=True)
class Item:
    description: str = ""
    always_show_description: bool = False
    exit_after_action: bool = False


@dataclass(kw_only=True)
class RunFunctionItem(Item):
    function: Callable[..., None]
    args: Tuple = ()
    kwargs: Dict[str, Any] = field(default_factory=dict)


@dataclass(kw_only=True)
class EditItem(Item):
    value: str
    validator: Callable[[str], bool]
    allowed_human_readable: str = ""
    display_value: bool = True


@dataclass(kw_only=True)
class OptionItem(Item):
    value: Any
    displayed_value: str = ""

@dataclass(kw_only=True)
class SelectionItem(Item):
    value: Any
    options: OrderedDict[str, OptionItem]
    display_value: bool = True


@dataclass(kw_only=True)
class SubMenuItem(Item):
    menu: OrderedDict[str, Item]
