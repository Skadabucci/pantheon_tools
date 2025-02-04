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

## Detailed Installation Guide

Follow these steps to install and run Pantheon Tools:

1. **Download and Install Python 3.x**:
    - Go to the [Python official website](https://www.python.org/downloads/).
    - Download the latest version of Python 3.x for Windows.
    - Run the installer and follow the instructions. Make sure to check the box that says "Add Python to PATH".

2. **Downloading the Release Package**
    - Go to the [Pantheon Tools releases page](https://github.com/skadabucci/pantheon_tools/releases).
    - Select the latest release version (ex: v0.2.1).
    - Download the latest release version of the package (zip file).
    - Extract the contents of the zip file to a directory of your choice.
    - Open File Explorer and navigate to the directory where you extracted the zip file.
    - Shift + Right-click in the directory and select "Open PowerShell window here" or "Open in terminal".

3. **Set Up a Virtual Environment**:
    - In the PowerShell or Command Prompt window, type the following command and press Enter to create a virtual environment:
      ```sh
      py.exe -m venv venv
      ```
    - Activate the virtual environment:
      ```sh
      .\venv\Scripts\activate
      ```

4. **Install Required Packages**:
    - In the activated virtual environment, type the following command and press Enter to install the required packages:
      ```sh
      py.exe -m pip install -r requirements.txt
      ```

5. **Select an application below to run**
    - Try for the experience prediction or macro maker applications. (run the commands in the **Usage** sections)

## Usage

### ExperiencePrediction
This tool runs continuously and makes predictions on how much XP you gain per kill. It does some simple screen-scraping to find the XP bar and then calculate changes.

```sh
py.exe -m pantheon_tools.ExperiencePrediction
```

#### Assumptions

When using the ExperiencePrediction tool, please note the following assumptions:

1. **XP Bar Opacity**: Your XP bar must be set to 100% opacity for the script to work correctly. Variations in color due to opacity changes can affect the accuracy of the tool.
2. **Screen Position**: The tool works best when the XP bar is positioned at the bottom of the monitor. Initial scans are performed from the bottom up.
3. **Techniques**: The tool does not use advanced image processing techniques such as grayscale, median filters, binarization, or tesseract post-processing.

#### Troubleshooting

If the XP bar is not being detected, try the following steps:

- Ensure the entire XP bar is visible on the screen.
- Position the XP bar at the bottom of the screen for optimal detection.
- Do not move the XP bar once the program has started. If you need to move it, restart the program.


#### Configuration Parameters

The following configuration parameters are used in the ExperiencePrediction tool:

- `EXPERIENCE_COLOR`: A tuple representing the RGB color values of the experience bar. Default is `(42, 99, 216)`.
- `EXPERIENCE_DIVIDER_COLOR`: A tuple representing the RGB color values of the experience divider. Default is `(155, 176, 237)`.
- `DARK_BLUE_COLOR`: A tuple representing the RGB color values of the dark blue color used in the UI. Default is `(0, 34, 64)`.
- `LIGHT_BLUE_COLOR`: A tuple representing the RGB color values of the light blue color used in the UI. Default is `(153, 166, 192)`.

- `DEAD_PLAYER_THRESHOLD`: A float value representing the threshold to determine if a player is dead and lost a level. Default is `70.0`.
- `SLEEP_TIME`: An integer representing the sleep time in seconds between each screen-scraping iteration. Default is `1`.
- `STARTUP_DELAY`: An integer representing the delay in seconds before the tool starts running. Default is `5`.
- `XP_BAR_BLOCKED_TOLERANCE`: An integer representing the tolerance level for detecting if the XP bar is blocked. Default is `0.99`.

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
* Optionally release this as a windows package (msi/exe)
* Tests
* ExpTracker
  * Handle the bug where users minimize the game or have a full screen app over Pantheon
  * Have console output rewrite itself to screen instead of printing constantly
  * Add Exp per hour tracking
  * ~~Handle level ups!!! if you go from ~99% to ~1% you should get a ding!~~
* MacroMaker
  * Turn the create_macro function into a Class for better handling of the object (ie: keeping wait times in float form and writing the file at the end of creation).
  * Have one spellbook and associate chapters of a spellbook with classes.
  * While creating a macro for a specific class, take into account external resources such as Focus (for wizards), Readiness, Mana, etc.
* BagSorter
  * Implement a script to sort bags
