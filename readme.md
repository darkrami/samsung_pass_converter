# Samsung Pass Converter

This script decrypts Samsung Pass `.spass` export files and converts them into a standard CSV format for easy import.

## Features

- Decrypts `.spass` files exported from Samsung Pass, using the password provided during export.
- Exports credentials to a CSV file.
- Provides both a command-line interface and a graphical user interface (GUI).
- Supports system-wide dark mode and manual theme switching.

## Requirements

- Python 3.6+
- `cryptography` library
- `sv-ttk` for GUI theming
- `darkdetect` for system theme detection

Install dependencies:

```sh
pip install cryptography sv-ttk darkdetect
```

## GUI Application

For a more user-friendly experience, you can use the GUI application.

### Running the GUI

Run the `gui.py` file from your terminal:
```sh
python gui.py
```

### GUI Features

*   **Modern UI:** A clean user interface with a modern look and feel.
*   **Icon Buttons:** Clear icons for all actions.
*   **Dark Mode:** Automatically detects your system's theme and includes a button (☀️/🌙) to toggle manually.
*   **File Selection:** Easily browse for your `.spass` export file.
*   **Password Entry:** A secure field to enter your decryption password.
*   **Output Directory:** Choose where you want to save the converted files.
*   **Custom Filename:** Optionally specify a custom name for the output CSV file. Defaults to `spass.csv`.
*   **Simple Feedback:** Get a clear "Success!" or "Something went wrong :(" message after conversion.

## Command-Line Usage

If you prefer to use the command line:

```sh
python convert.py <export_file_path> <password> [--output-dir <directory>] [--output-filename <filename>]
```

- **`<export_file_path>`**: Path to your `.spass` file.
- **`<password>`**: Password used while exporting Samsung Pass content.
- **`--output-dir <directory>`**: (Optional) Specify a directory to save the output file. Defaults to the same directory as the input file.
- **`--output-filename <filename>`**: (Optional) Specify a name for the output CSV file. Defaults to `spass.csv`.

### This will produce:

- A CSV file (e.g., `spass.csv` or your custom name).

## Building from Source

If you want to build the executable from the source code yourself, you can do so by following these instructions. This is necessary if you want to run the application as a standalone `.exe` file on Windows without installing Python and the dependencies manually.

### On Windows (Easy Way)

Simply run the `build.bat` script by double-clicking it. It will automatically:
1. Create a Python virtual environment.
2. Install all necessary dependencies.
3. Run PyInstaller to create the executable.

After the script finishes, you will find the `SamsungPassConverter.exe` file in the `dist` folder.

### On Windows (Manual Way)

If you prefer to run the steps manually, open a Command Prompt and follow these steps:

1.  **Install Python:** Make sure you have Python 3.6+ installed. You can get it from [python.org](https://www.python.org/).

2.  **Create a virtual environment:**
    ```sh
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    ```sh
    venv\Scripts\activate.bat
    ```

4.  **Install dependencies:**
    ```sh
    pip install cryptography sv-ttk darkdetect pyinstaller
    ```

5.  **Run PyInstaller:**
    ```sh
    pyinstaller --onefile --windowed --name "SamsungPassConverter" gui.py
    ```

6.  **Find the executable:** The `SamsungPassConverter.exe` file will be in the `dist` folder.


## Legal Notice

This script is intended for personal use to migrate your own data from Samsung Pass.
Do not use this tool on files you do not own or have permission to access.

## Disclaimer

This project is not affiliated with, endorsed by, or supported by Samsung.
Use at your own risk.
