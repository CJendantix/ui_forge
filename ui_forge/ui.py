from collections import OrderedDict
import curses
from typing import Any, Callable, Dict, Tuple
from . import selector, common, actions, items


def dict_ui(
    base_window: curses.window,
    dictionary: Dict[str, items.Item],
    item_display: Callable[
        [Tuple[str, items.Item], bool], Tuple[str, int]
    ] = common.default_item_display,
    start_line: int = 0,
    start_pos: int = 0,
):
    while True:
        base_window.clear()
        base_window.refresh()

        item, (start_line, start_pos) = selector.dict_select(
            base_window,
            OrderedDict(dictionary),
            item_display,
            start_line=start_line,
            start_pos=start_pos,
        )

        if isinstance(item[1], items.RunFunctionItem):
            actions.run_function(item[1])
        elif isinstance(item[1], items.SelectionItem):
            item[1].value = actions.select(base_window, item[1].options, item_display)
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
    ] = common.default_item_display,
    start_line: int = 0,
    start_pos: int = 0,
) -> Any:
    value = actions.select(base_window, options, item_display, start_line, start_pos)
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
    value = actions.edit(
        base_window, (name, items.EditItem(value=value, validator=validator))
    )
    base_window.clear()
    base_window.refresh()
    return value
