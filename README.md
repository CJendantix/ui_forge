# Curses UI
An easy-to-use procedurally-generated widget system for curses in Python.

## item format:

item format is the main format used by the majority of widgets in this system.

### definitions
An "arg," from here on out, is a key-value pair, from within a dictionary, that is itself a value of a dictionary in item format

A sub arg is an arg that is only passed with a certain functionality
sub args are required unless otherwise specified

#### global args
These arguments will be on *every* item listed here, optionally unless otherwise specified.
- `functionality: str` - the functionality of the item, valid values will be covered later. Invalid values will do the same as not specifying at all.
- `description: str` - a description of the option
- `always_show_description: bool` - whether or not to always show the description of the item, if set to `False`, the description will only be shown while the item is selected.
- `exit_after_action` - exits the current menu after the option is selected and its functionality is performed. Can be used with the `none` functionality to implement an exit button.

## dict_ui
Arguments:
- `base_window: curses.window` - a curses window
- `dictionary: dict[str, dict]` - a dictionary with values of dicts in item format. This is what the UI is generated from.
- `item_display: Callable[[tuple[str, dict], bool], tuple[str, int]]` *optional* - an argument that allows users to overwrite the way items are listed

#### functionalities
- `run_function`
    Runs a function with arbitrary arguments
    
    Sub Args:
    - `function: Callable[[Unknown], None]` - a reference to the function to run
    - `args: list` *optional* - a list of positional arguments to pass to the function
    - `kwargs: dict[str, Unknown]` *optional* - a dictionary of keyword arguments to pass to the function
- `edit`
    Opens the editor widget. The `name` argument of the selection widget is the key of this item.
    
    Sub Args:
    - `value: str` - as if you were passing it directly to the selection widget, format covered below. This gets overwritten after a successful edit.
    - `validator: Callable[[str], bool]` *optional* - as if you were passing it directly to the selection widget, format covered below.
    - `allowed_human_readable: str` *optional* - as if you were passing it directly to the selection widget, format covered below.
- `select`
    Opens the selection widget

    sub args:
    - `value: str` - as if you were passing it directly to the selection widget, format covered below. This gets overwritten when the user selects a new value.
    - `options: dict[str, dict]` - as if you were passing it directly to the selection widget, format covered below.
- `sub menu`
    A new instance of `dict_ui` with the input menu dictionary

    Sub Args:
    - `menu: dict` - a menu dictionary

## selection_ui
Arguments:
- `base_window: curses.window` - a curses window
- `options: dict[str, dict]` - a dictionary containing dictionaries in item format. All global args are valid, but functionality does nothing.
- `item_display: Callable[[tuple[str, dict], bool], tuple[str, int]]` *optional* - an argument that allows users to overwrite the way items are listed

## editor_ui
- `base_window: curses.window` - a curses window
- `name: str` - the "name" of the value being assigned, ususally analagous to the name of the variable being assigned to. This gets displayed to the user
- `value: str` *optional* - the default value before modification
- `validator: Callable[[str], bool]` *optional* - a reference to a function. The input is the entire submitted string, and the output will determine whether or not it will get accepted. If it does not get accepted, the input box will be reset to the previous value, and the user will be prompted to input again. This will repeat until the uset inputs a valid value.
- `allowed_human_readable: str` *optional* - a string that gets printed after the name of the value the user is editing. This is intended to instruct users in an understandable fashion what values are valid or invalid.