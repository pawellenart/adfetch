# ADFetch Console Application

ADFetch is a Python-based console application that allows to browse and download ADF files using an interactive and user-friendly text-based interface. The application supports listing and filtering files based on their starting letters and includes functionality for refreshing the file cache from a specified URL.

### Key Features

1. **Navigate Items**: Use the arrow keys to navigate through the menu. Press `Enter` to select an option.
2. **Refresh Cache**: Update the cache from the specified URL by selecting the "Refresh cache" button.
3. **Browse Files**: Select a letter or "0-9" to list items starting with that character.
4. **Download Files**: Choose an item to download it to the specified target directory.
5. **Exit the Application**: Press `F10` to quit the application.

### Customizing Inputs
- **Target Directory**: Edit the "Target ADF download directory" field to set the directory where files will be saved.
- **Cache URL**: Edit the "ADF cache source" field to change the URL for refreshing the cache.

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Create and activate a virtual environment (optional but recommended):

  * On Windows:
    ```bash
    python -m venv
    venv venv\\Scripts\\activate
    ```

  * On macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) Generate standalone binary:
    ```bash
    pip install pyinstaller
    pyinstaller --onefile main.py
    ```

## Usage

Run the application using:
```bash
python main.py
```

## Dependencies

- [urwid](https://urwid.org/): For building the console-based UI.
- [requests](https://docs.python-requests.org/): For fetching data from the specified URL.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

Special thanks to the creators of `urwid` and `requests` for their excellent libraries.
