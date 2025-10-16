# AutoPaster v1.0

AutoPaster is a Windows application that automatically pastes clipboard content into a specified Chrome browser tab (like Google Gemini) using customizable hotkeys. It supports multiple Chrome profiles, tab groups, and multi-monitor setups.

## Features

-  **Customizable Hotkeys**: Set any key combination for activation
-  **Smart Tab Detection**: Automatically finds target tabs in Chrome across multiple profiles
-  **Multi-Profile Support**: Works with multiple Chrome profiles and instances
-  **Tab Group Navigation**: Handles Chrome tab groups and complex tab arrangements
-  **Multi-Monitor Support**: Works across multiple monitors and screen configurations
-  **Enhanced Paste Methods**: Multiple paste strategies for better compatibility with different interfaces
-  **Simple GUI**: Easy-to-use interface for configuration
-  **Background Operation**: Runs efficiently without slowing down the system

## Installation & Running

### Method 1: Using Executable (Fastest - Recommended)

Navigate to project directory and run the executable:

```cmd
cd /d "D:\Programing\0. Projects\AutoPaster"
dist\AutoPaster.exe
```

### Method 2: Using Virtual Environment (For Development)

1. **Navigate to Project Directory**:

   ```cmd
   cd /d "D:\Programing\0. Projects\AutoPaster"
   ```

2. **Activate Virtual Environment**:

   ```cmd
   venv\Scripts\activate
   ```

3. **Run Application**:
   ```cmd
   python gui.py
   ```

### Method 3: Using System Python

1. **Navigate to Project Directory**:

   ```cmd
   cd /d "D:\Programing\0. Projects\AutoPaster"
   ```

2. **Run Application**:
   ```cmd
   python gui.py
   ```

### Method 4: Fresh Installation

If dependencies are not installed:

1. **Install Python**: Ensure Python 3.7+ is installed
2. **Create Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run Application**:
   ```bash
   python gui.py
   ```

### Method 5: Manual Dependency Installation

If requirements.txt is not available, install these dependencies:

```bash
pip install pyperclip==1.9.0
pip install pyautogui==0.9.54
pip install pynput==1.8.1
pip install pywinauto==0.6.9
```

Then run:

```bash
python gui.py
```

## Usage

1. **Launch**: Run `gui.py`
2. **Set Target Tab**: Enter tab title in "Target Tab Title" field (default: Gemini)
3. **Set Hotkey**: Enter desired key combination (default: F1)
4. **Start**: Click "Start" button
5. **Use**:
   -  Copy text (Ctrl+C)
   -  Press your hotkey
   -  Text automatically pastes into the target tab

## Hotkey Format

### Single Keys:

-  `f1`, `f2`, ..., `f12`
-  `space`, `enter`, `esc`, `backspace`
-  Letters/numbers: `a`, `b`, `1`, `2`, ...

### Key Combinations:

-  `ctrl_l + c` (Left Ctrl + C)
-  `alt_r + 1` (Right Alt + 1)
-  `ctrl_l + shift + s` (Left Ctrl + Shift + S)
-  `alt_l + shift + f12` (Left Alt + Shift + F12)

### Common Key Names:

-  **Control**: `ctrl_l`, `ctrl_r`
-  **Alt**: `alt_l`, `alt_r`
-  **Shift**: `shift_l`, `shift_r`
-  **Function Keys**: `f1`, `f2`, ..., `f12`
-  **Special Keys**: `space`, `enter`, `esc`, `backspace`

## Building Executable

To create an executable (.exe) file using PyInstaller:

```bash
pip install pyinstaller
pyinstaller AutoPaster.spec
```

The executable will be created in the `dist` folder.

## System Requirements

-  **OS**: Windows
-  **Python**: Version 3.7 or higher
-  **Browser**: Google Chrome (must be running)
-  **Permissions**: Requires clipboard and keyboard control access

## Troubleshooting

### Common Issues:

1. **"No active Chrome window found"**:

   -  Ensure Chrome is open
   -  At least one tab must be open

2. **"Could not find tab"**:

   -  Enter exact tab title
   -  Ensure target tab is open in Chrome

3. **Hotkey not working**:
   -  Check key format
   -  Ensure program is in "Running" state

## Important Notes

-  Only works with Google Chrome
-  Optimized for Google Gemini but works with any Chrome tab
-  Supports multiple Chrome profiles and tab groups
-  Works across multiple monitors and screen configurations
-  Avoid fullscreen Chrome for better performance
-  Requires system security permissions
-  Restart application if it closes unexpectedly

## Support

If you encounter issues, check:

1. All dependencies are installed
2. Chrome is open and accessible
3. Hotkey format is correct
4. Application is in "Running" state
