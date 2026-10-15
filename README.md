# AutoPaster (Gemini version)

An intelligent and fast tool for automatically copying and pasting text from any application to a specific tab in Google Chrome browser, with just a custom hotkey.

![GIF of AutoPaster in action] (Suggestion: Place a short GIF showing how the program works here to make it more impactful)

## Key Features 🚀

-  **Complete Automation**: Fully automate the process of finding tabs and pasting text.
-  **Custom Hotkey**: Define any key or key combination that you're comfortable with as a shortcut.
-  **Complex Environment Support**: Works well with multiple Chrome windows, multiple profiles, and multi-monitor setups.
-  **Smart Search**: Reads the titles of all Chrome windows instantly, without focusing them or pressing any keys, and goes straight to the most recently used window (in any profile) that is showing the target tab. Only if no window is showing it does it cycle through tabs with Ctrl+Tab, starting with the window it pasted into last time.
-  **Precise Click and Paste**: Intelligently clicks at a specified point in the tab, moves to the end of the existing text, and pastes the text as plain text with an initial space.
-  **Speed Optimized**: Detects a new clipboard text within ~10 ms, sends keystrokes with no hidden pauses, and moves on as soon as Chrome switches tabs instead of waiting a fixed time.

## How It Works ⚙️

1. You define a hotkey (e.g., F1) and the target tab title (e.g., Google Gemini) in the program.
2. Press the **Start** button. The program waits in the background.
3. Press your hotkey.
4. Within ~7.5 seconds, copy a text in any application (e.g., ShareX or anywhere else). Only text copied **after** the hotkey is pasted; whatever was already in the clipboard is ignored.
5. The program automatically finds the Chrome window and target tab, focuses on it, clicks the input box, goes to the end of the text, adds a space, and pastes the text!

## Requirements 📦

To run this project from source, the following libraries must be installed (pywin32 is installed automatically with pywinauto):

```bash
pip install -r requirements.txt
```

## Usage Guide 📋

1. Run the program:

   -  **Option 1 (no Python needed):** run `dist/AutoPaster(Gemini_version).exe`
   -  **Option 2:** run the script with Python:

   ```bash
   python gui.py
   ```

2. Enter the exact title of your target tab in the **Target Tab Title** field.
3. Enter your desired hotkey in the **Shortcut** field (e.g., `f1` or `ctrl_l + a`).
4. Click the **Start** button.
5. The program is now ready to work in the background!

### Build the exe 🏗️

```bash
pip install pyinstaller
pyinstaller AutoPaster.spec
```

The executable is created in the `dist` folder.

## Technologies Used 🛠️

-  **Tkinter**: For building the graphical user interface (GUI)
-  **pywinauto**: For focusing and managing Windows windows
-  **pywin32 (win32gui)**: For fast enumeration of Chrome windows and reading their titles
-  **pynput**: For global listening and keyboard key management
-  **pyautogui**: For precise simulation of clicks and key presses
-  **pyperclip**: For interacting with the operating system clipboard
-  **Windows clipboard sequence number (ctypes)**: For detecting clipboard changes instantly without repeatedly opening the clipboard
