# Curses UI
An easy-to-use procedurally-generated widget system for curses in Python.

## Item Format
The format used across the majority of all widgets in this system.

### clarification
An "arg," from here on out, is a key-value pair, from within a dictionary, that is itself a value of a key-value pair from within the dictionary passed to `dict_ui`

A sub arg is an arg that is only passed with a certain functionality

Every arg besides `functionality` that is not already a dict alone, is a dict with the key `"value"` pointing to your expected value, to allow for interior mutability by outside functions

### global args
These arguments will be on *every* item, optionally unless stated otherwise.
- `functionality: str` **required** - the functionality of the item, valid values will be covered later. Example: `"functionality": "none"`. Program will most likely panic if not provided.
- `description: dict[str, str]` - a description of the option. Example : `"description": {"value": "description"}`. No description is displayed if not provided.
- `always_show_description: dict[str, bool]` - whether or not to always show the description of the item, if set to `False`, the description will only be shown while the item is selected. Example: `"always_show_description": {"value": True}`. Defaults to False
- `exit_after_action: dict[str, bool]` - whether or not to exit the current menu after the functionality has completed. Example: `"exit_after_action": {"value": True}`. Defaults to False

## dict_ui
Arguments:
- `base_window: curses.window` - a curses window
- `dictionary: dict` - a dictionary following a specific format. This is what the UI is generated from
- `item_display: Callable[[tuple[str, dict], bool], tuple[str, int]]` - an optional keyword argument that allows users to overwrite the way items are listed. See `default_item_display` in `ui_forge.common`.

### functionalities
- `none`
    displays the value without doing anything apon selection, unless a global argument causes it to (`exit_after_action`, for example)
- `run_function`
    runs a function
    
    sub args:
    - `function: dict[str, Callable[[Unknown], None]]` - a reference to the function to run. Example: `"function": {"value": lambda x,y=1 : x+y}`
    - `args: dict[str, list]` - a list of positional arguments to pass to the function. Example: `"args": {"value": [1]}`
    - `kwargs: dict` - a dictionary of keyword arguments to pass to the function. Example: `"kwargs": {"y": 2}`
- `edit`
    opens the editor widget for an assigned value
    
    sub args:
    - `value: dict[str, str]` - the value assigned before editing - this gets overwritten after a successful edit. Example: `"value": {"value": "a"}`
    - `validator: dict[str, Callable[[str], bool]]` - a reference to a function. The input is the entire submitted string, and the output will determine whether or not it will get accepted. If it does not get accepted, the input box will be reset to the previous value, and the user will be prompted to input again. This will repeat until the uset inputs a valid value. Example: `"validator": {"value": lambda x : x}`
    - `allowed_human_readable: dict[str, str]` - a string that gets printed after the name of the value the user is editing. This is intended to instruct users in an understandable fashion what values are valid or invalid. Example: `"allowed_human_readable": {"value": "only integers allowed"}`
- `select`
    opens the selection widget

    sub args:
    - `value: dict[str, str]` - the value assigned before editing - this gets overwritten when the user selects a new value. Example: `"value": {"value": "a"}`
    - `options: dict` -  a dictionary containing dictionaries with the `option` functionality. Example: `"options": {"a": {"functionality": "option"}, "b": {"functionality": "option"}, "c": {"functionality": "option"}}`
- `option`
    an option in a selection menu. Only intended to be used within the selection widget. The key is the value that will be selected.
- `sub menu`
    a new instance of `dict_ui` with the input dictionary

    sub args:
    - `menu: dict`: a menu dictionary. equivalent to anything passed to `dict_ui`

## selection_ui
Arguments:
- `base_window: curses.window` - a curses window
- `options: dict` - a dictionary containing `option` items
- `item_display: Callable[[tuple[str, dict], bool], tuple[str, int]]` - an optional keyword argument that allows users to overwrite the way items are listed

## editor_ui
- `base_window: curses.window` - a curses window
- `name: str` - the "name" of the value being assigned,  ususally analagous to the name of the variable being assigned to. This gets displayed to the user
- `value: str` - the default value before modification
- `validator: Callable[[str], bool]` - a reference to a function. The input is the entire submitted string, and the output will determine whether or not it will get accepted. If it does not get accepted, the input box will be reset to the previous value, and the user will be prompted to input again. This will repeat until the uset inputs a valid value.
- `allowed_human_readable: str` - a string that gets printed after the name of the value the user is editing. This is intended to instruct users in an understandable fashion what values are valid or invalid.