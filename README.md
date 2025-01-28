# Pantheon Tools 
Pantheon Tools is a set of python scripts that help automate some of the tedious tasks in Pantheon Rise of the Fallen.

## Requirements

- Python 3.x
- Git

## Installation

1. Clone the repository:
    ```sh
    git clone <url>
    cd pantheon_tools
    py.exe -m venv venv
    .\\venv\\Scripts\\activate
    py.exe -m pip install -r requirements.txt
    ```

## Usage

### ExperiencePrediction
This tool runs continuously and makes predictions on how much XP you gain per kill. It does some simple screen-scraping to find the XP bar and then calcualte changes.

```sh
py.exe -m pantheon_tools.ExperiencePrediction
```

#### Assumptions
Note there are a assumptions when using this tool. Your XP bar MUST be 100% opacity for this script to work. Otherwise it will vary too much in color. I don't use any techniques like grayscale, median filters, binarization, or tesseract post processing. Also It will typically work better if it is at the bottom of the monitor.

#### Configuration Parameters

The following configuration parameters are used in the ExperiencePrediction tool:

- `EXPERIENCE_COLOR`: A tuple representing the RGB color values of the experience bar. Default is `(42, 99, 216)`.
- `EXPERIENCE_DIVIDER_COLOR`: A tuple representing the RGB color values of the experience divider. Default is `(155, 176, 237)`.
- `DARK_BLUE_COLOR`: A tuple representing the RGB color values of the dark blue color used in the UI. Default is `(0, 34, 64)`.
- `LIGHT_BLUE_COLOR`: A tuple representing the RGB color values of the light blue color used in the UI. Default is `(153, 166, 192)`.

- `DEAD_PLAYER_THRESHOLD`: A float value representing the threshold to determine if a player is dead and lost a level. Default is `70.0`.
- `SLEEP_TIME`: An integer representing the sleep time in seconds between each screen-scraping iteration. Default is `1`.

### MacroMaker 
Macro is a Python script that allows you to create and manage spellbooks for different classes and generate macros based on the spells in the spellbook.

To run the script, navigate to the git directory and execute the following command:

```sh
py.exe -m pantheon_tools.MacroMaker
```

### Options

When you run the script, you will be presented with the following options:

1. **Load from an existing file**: Load an existing spellbook from a JSON file.
2. **Start a new spellbook**: Create a new spellbook from scratch.

### Creating a Spellbook

If you choose to start a new spellbook, you will be prompted to enter the class name and the file path to save the spellbook. You can then add spells interactively by providing the following details for each spell:

- Spell name
- Cast time
- Spell type (1: use, 2: technique, 3: utility)
- Spell location
- Cooldown (default is 0.0)
- Has global cooldown (yes/no, default is yes)

You can also list existing spells or quit the interactive mode at any time.

### Saving the Spellbook

Once you have added all the spells, the spellbook will be saved to the specified file path.

### Creating a Macro

After creating or loading a spellbook, you will be prompted to create a macro. If you choose to create a macro, you will be asked to rank the spells in order of importance and specify the number of spells to include in the macro. The macro will then be generated and saved to the specified file path.

## Example

Here is an example of how to use the script:

1. Run the script:
    ```sh
    python MacroMaker.py
    ```

2. Choose to start a new spellbook:
    ```
    Please choose an option:
      1. Load from an existing file
      2. Start a new spellbook
    Enter 1, or 2: 2
    ```

3. Enter the class name and file path:
    ```
    Enter the class name for the spellbook: Mage
    Enter file path to save the spellbook: mage_spellbook.json
    ```

4. Add spells interactively:
    ```
    Enter spell name (or 'quit' to finish): Fireball
    Enter cast time: 2.5
    Enter spell type (1: use, 2: technique, 3: utility): 1
    Enter spell location: 1
    Enter cooldown (default 0.0): 0.0
    Has global cooldown? (yes/no, default yes): yes
    ```

5. Save the spellbook and create a macro:
    ```
    Enter file path to save the spellbook: mage_spellbook.json
    Spellbook saved to mage_spellbook.json

    Would you like to create a macro? (y/n).
    Enter y or n: y
    ```

## License

This project is licensed under the MIT License.

## Backlog / Wishlist
* Tests
* MacroMaker
  * Turn the create_macro function into a Class for better handling of the object (ie: keeping wait times in float form and writing the file at the end of creation).
  * Have one spellbook and associate chapters of a spellbook with classes.
  * While creating a macro for a specific class, take into account external resources such as Focus (for wizards), Readiness, Mana, etc.
* BagSorter
  * Implement a script to sort bags
