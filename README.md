# Curses UI
An easy-to-use procedurally-generated widget system for curses in Python.

## dict_ui
Arguments:
- `base_window: curses.window` a curses window
- `dictionary: dict` a dictionary following a specific format. This is what the UI is generated from
- `item_display: Callable[[tuple[str, dict], bool], tuple[str, int]]` an optional keyword argument that allows users to overwrite the way items are listed

### dictionary format:
An "arg," from here on out, is a key-value pair, from within a dictionary, that is itself a value of a key-value pair from within the dictionary passed to `dict_ui`

A sub arg is an arg that is only passed with a certain functionality

#### global args
These arguments will be on *every* item listed here.
- `functionality: str` **required** - the functionality of the item, valid values will be covered later
- `description: str` - a description of the option
- `always_show_description: bool` - whether or not to always show the description of the item, if set to `False`, the description will only be shown while the item is selected.

#### functionalities
- `quit`
    exits this instance of a menu. if selected in a sub menu it will return the user to the previous menu
- `run_function`
    runs a function
    
    sub args:
    - `function: Callable[[Unknown], None]` - a reference to the function to run
    - `args: list | tuple` - a list or tuple of positional arguments to pass to the function
    - `kwargs: dict` - a dictionary of keyword arguments to pass to the function
- `edit`
    opens the editor widget for an assigned value
    
    sub args:
    - `value: str` - the value assigned before editing - this gets overwritten after a successful edit
    - `validator: Callable[[str], bool]` - a reference to a function. The input is the entire submitted string, and the output will determine whether or not it will get accepted. If it does not get accepted, the input box will be reset to the previous value, and the user will be prompted to input again. This will repeat until the uset inputs a valid value.
    - `allowed_human_readable: str` - a string that gets printed after the name of the value the user is editing. This is intended to instruct users in an understandable fashion what values are valid or invalid.
- `select`
    opens the selection widget

    sub args:
    - `value: str`
        the value assigned before editing - this gets overwritten when the user selects a new value
    - `options: dict`:
        a dictionary containing dictionaries with the `option` functionality
- `option`
    an option in a selection menu. Only intended to be used within the selection widget. The key is the value that will be selected.
- `sub menu`
    a new instance of `dict_ui` with the input dictionary

    sub args:
    - `menu: dict`
        a menu dictionary

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