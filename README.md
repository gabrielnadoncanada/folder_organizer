# Desktop File Organizer

## Introduction
Desktop File Organizer is a Python Tkinter-based application designed to help users efficiently organize their files and folders. It categorizes files by their types into separate folders, provides options for backing up files before organization, and features a robust undo functionality that allows users to revert to a specific organization state based on historical actions.

## Features
- **File Organization**: Automatically sorts files into folders based on file extensions.
- **Backup Creation**: Option to create a backup of files before organizing them, stored with a timestamp for easy recovery.
- **Undo Functionality**: Allows users to select and undo organization actions from a history of changes, reverting files to their previous states.
- **Interactive GUI**: User-friendly graphical interface that makes it easy to use and accessible for all users.
- **Customizable Exclusions**: Exclude specific files from being organized, such as the script file itself.

## Installation

1. **Clone the Repository**: 
git clone https://github.com/yourusername/desktop-file-organizer.git

2. **Navigate to the Project Directory**:
cd desktop-file-organizer

## Dependencies
Ensure you have Python installed along with Tkinter. Install Python and Tkinter if they are not installed:
- For most systems, Tkinter is included with the standard Python installation.
- You can install Python from [python.org](https://www.python.org/downloads/).

## Usage

Run the application by executing the script in Python:

```bash
python folder_organizer_gui.py
```

## Use the GUI to:

1. Choose the folder you want to organize by clicking the "Browse" button.
2. Select whether to back up files before organizing.
3. Click "Organize" to start the organization process.
4. View past organization actions in the list box and select a specific action to undo if necessary.