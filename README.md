# ui_forge Package Documentation

## Submodules

### ui_forge.actions Module

#### `ui_forge.actions.edit(base_win: window, item: Tuple[str, EditItem]) → str`
Opens an editor interface for modifying the value of an `EditItem` and returns the validated input from the user.

#### `ui_forge.actions.run_function(item: RunFunctionItem)`
Executes the function associated with the specified `RunFunctionItem`. This item should not return a value.

#### `ui_forge.actions.select(base_win: window, options: OrderedDict[str, OptionItem], item_display: Callable[[Tuple[str, Item], bool], Tuple[str, int]], start_line: int = 0, start_scroll: int = 0) → Any`
Displays a selection menu using the provided options and returns the value of the selected `OptionItem`.

### ui_forge.items Module

#### `class ui_forge.items.Item(*, description: str = '', always_show_description: bool = False, exit_after_action: bool = False)`
Bases: `object`

Base class for menu items, providing basic attributes and functionality.

#### `class ui_forge.items.EditItem(*, description: str = '', always_show_description: bool = False, exit_after_action: bool = False, value: str, validator: Callable[[str], bool] = lambda _: True, allowed_human_readable: str = '', display_value: bool = True)`
Bases: [`Item`](#class-ui_forgeitemsitem-description-str---always_show_description-bool--false-exit_after_action-bool--false)

Represents an item that allows users to edit a value.

**Args:**
- `value (str)`: The current value, which will be overwritten.
- `validator (Callable[[str], bool])`: Function to validate the user input; defaults to always accepting the value.
- `header (str)`: A header above what the user is editing; defaults to an empty string.
- `display_value (bool)`: Determines if the value is shown in the main interface; defaults to True.

**Args:**
- `description (str)`: A brief description of the item; defaults to an empty string.
- `always_show_description (bool)`: Indicates if the description should always be visible; defaults to False.
- `exit_after_action (bool)`: Indicates if the menu should exit after this item is selected; defaults to False.

#### `class ui_forge.items.OptionItem(*, description: str = '', always_show_description: bool = False, exit_after_action: bool = False, value: Any, displayed_value: str = '')`
Bases: [`Item`](#class-ui_forgeitemsitem-description-str---always_show_description-bool--false-exit_after_action-bool--false)

Represents an option in a selection menu.

**Args:**
- `value (Any)`: The actual value of the option.
- `displayed_value (str)`: The string to display for the option; defaults to an empty string.

#### `class ui_forge.items.RunFunctionItem(*, description: str = '', always_show_description: bool = False, exit_after_action: bool = False, function: Callable[..., None], args: Tuple = (), kwargs: Dict[str, Any] = {})`
Bases: [`Item`](#class-ui_forgeitemsitem-description-str---always_show_description-bool--false-exit_after_action-bool--false)

Represents an item that executes a specified function when selected.

**Args:**
- `function (Callable[..., None])`: The function to run; it must not return a value.
- `args (Tuple[Any, ...])`: Arguments to pass to the function; defaults to an empty tuple.
- `kwargs (Dict[str, Any])`: Keyword arguments for the function; defaults to an empty dictionary.

#### `class ui_forge.items.SelectionItem(*, description: str = '', always_show_description: bool = False, exit_after_action: bool = False, value: Any, options: OrderedDict[str, OptionItem], display_value: bool = True, start_line: int = 0, start_scroll: int = 0)`
Bases: [`Item`](#class-ui_forgeitemsitem-description-str---always_show_description-bool--false-exit_after_action-bool--false)

Represents an item that allows the user to select from multiple options.

**Args:**
- `value (Any)`: The currently selected value.
- `options (OrderedDict[str, OptionItem])`: Available options for selection.
- `display_value (bool)`: Determines if the value is displayed in the main interface; defaults to True.
- `start_line (int)`: The initial line selected in the options; defaults to 0.
- `start_scroll (int)`: The initial scroll position; defaults to 0.

#### `class ui_forge.items.SubMenuItem(*, description: str = '', always_show_description: bool = False, exit_after_action: bool = False, menu: OrderedDict[str, Item])`
Bases: [`Item`](#class-ui_forgeitemsitem-description-str---always_show_description-bool--false-exit_after_action-bool--false)

Represents a submenu that contains additional items.

**Args:**
- `menu (OrderedDict[str, Item])`: A collection of items that make up the submenu.

### ui_forge.selector Module

#### `class ui_forge.selector.Actions(value, names=<not given>, *values, module=None, qualname=None, type=None, start=1, boundary=None)`
Bases: `Enum`

Enumerates actions for the selector.

- `Action = 3`
- `Pass = 0`
- `Scroll_Down = 1`
- `Scroll_Up = 2`

#### `ui_forge.selector.dict_select(base_win: window, dictionary: OrderedDict[str, T], item_display: Callable[[Tuple[str, Item], bool], Tuple[str, int]], start_line: int = 0, start_scroll: int = 0) → Tuple[Tuple[str, T], Tuple[int, int]]`
Displays a selection interface using a dictionary of items and returns the selected item and its position.

#### `ui_forge.selector.display_dict(pad: window, dictionary: OrderedDict[str, T], selected_line: int, item_display: Callable[[Tuple[str, T], bool], Tuple[str, int]])`
Renders a dictionary of items in the specified window, highlighting the selected line.

#### `ui_forge.selector.get_max_display_length(dictionary: dict, item_display: Callable[[Tuple[str, T], bool], Tuple[str, int]]) → int`
Calculates the maximum display length of items in a dictionary based on the provided display function.

#### `ui_forge.selector.process_command(command: int, Keymap: Keymap = Keymap(Up=[259], Down=[258], Action=[10])) → Actions`
Processes a user command and returns the corresponding action.

#### `ui_forge.selector.scroll_down(current_line: int, scroll: int, max_scroll: int, window_top: int, window_bottom: int, offset: int = 2) → Tuple[int, int]`
Handles scrolling down in the selection menu and returns updated line and scroll positions.

#### `ui_forge.selector.scroll_up(current_line: int, scroll: int, offset: int = 2) → Tuple[int, int]`
Handles scrolling up in the selection menu and returns updated line and scroll positions.

### ui_forge.ui Module

#### `ui_forge.ui.dict_ui(base_window: window, ui: OrderedDict[str, Item], item_display: Callable[[Tuple[str, Item], bool], Tuple[str, int]] = default_item_display, start_line: int = 0, start_scroll: int = 0)`
Creates a user interface in a Curses window for interacting with an ordered dictionary of items.

**Args:**
- `base_window (curses.window)`: The Curses window for rendering the UI.
- `ui (OrderedDict[str, items.Item])`: An ordered dictionary of item names and their corresponding `Item` instances.
- `item_display (Callable[[Tuple[str, items.Item], bool], Tuple[str, int]], optional)`: Function to customize item display; defaults to `default_item_display`.
- `start_line (int, optional)`: Default selected line; defaults to 0.
- `start_scroll (int, optional)`: Default scroll position; defaults to 0.

#### `ui_forge.ui.editor_ui(base_window: window, name: str, value: str = '', validator: Callable[[str], bool] = lambda _: True, allowed_human_readable: str = '') → str`
Displays an editor interface for user input and returns the modified value.

**Args:**
- `base_window (curses.window)`: The Curses window for rendering the editor.
- `name (str)`: The prompt or title for the editor.
- `value (str, optional)`: Default value to display; defaults to an empty string.
- `validator (Callable[[str], bool], optional)`: Function to validate the input; defaults to a function that always accepts the value.
- `header (str, optional)`: A header above what the user is editing; defaults to an empty string.

**Returns:**
- `str`: The user-modified value after validation.

#### `ui_forge.ui.selection_ui(base_window: window, options: OrderedDict[str, OptionItem], item_display: Callable[[Tuple[str, Item], bool], Tuple[str, int]] = default_item_display, start_line: int = 0, start_scroll: int = 0) → Any`
Displays a selection menu in a Curses window for choosing from an ordered dictionary of options.

**Args:**
- `base_window (curses.window)`: The Curses window for rendering the selection menu.
- `options (OrderedDict[str, items.OptionItem])`: An ordered dictionary of option names and corresponding `OptionItem` instances.
- `item_display (Callable[[Tuple[str, items.Item], bool], Tuple[str, int]], optional)`: Function to customize item display; defaults to `default_item_display`.
- `start_line (int, optional)`: Default selected line; defaults to 0.
- `start_scroll (int, optional)`: Default scroll position; defaults to 0.

**Returns:**
- `Any`: The value of the selected `OptionItem`.
