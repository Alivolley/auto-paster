# AutoPaster (Gemini version)

An intelligent and fast tool for automatically copying and pasting text from any application to a specific tab in Google Chrome browser, with just a custom hotkey.

![GIF of AutoPaster in action] (Suggestion: Place a short GIF showing how the program works here to make it more impactful)

## Key Features 🚀

-  **Complete Automation**: Fully automate the process of finding tabs and pasting text.
-  **Custom Hotkey**: Define any key or key combination that you're comfortable with as a shortcut.
-  **Complex Environment Support**: Works well with multiple Chrome windows, multiple profiles, and multi-monitor setups.
-  **Smart Search**: Uses caching to instantly find the target tab in subsequent runs, significantly increasing work speed.
-  **Precise Click and Paste**: Intelligently clicks at a specified point in the tab and then pastes the text with an initial space.
-  **Speed Optimized**: With precise delay settings, operations are performed in the fastest possible time without errors.

## How It Works ⚙️

1. You define a hotkey (e.g., F1) and the target tab title (e.g., Google Gemini) in the program.
2. Press the **Start** button. The program waits in the background.
3. In any application (e.g., ShareX or anywhere else), copy a text.
4. Immediately press your hotkey.
5. The program automatically finds the Chrome window and target tab, focuses on it, clicks at the specified point, and pastes the text!

## Requirements 📦

To run this project, the following libraries must be installed:

```bash
pip install pyperclip pyautogui pynput pywinauto
```

## Usage Guide 📋

1. Run the script with Python:

```bash
python gui.py
```

2. Enter the exact title of your target tab in the **Target Tab Title** field.
3. Enter your desired hotkey in the **Shortcut** field (e.g., `f1` or `ctrl_l + a`).
4. Click the **Start** button.
5. The program is now ready to work in the background!

## Technologies Used 🛠️

-  **Tkinter**: For building the graphical user interface (GUI)
-  **pywinauto**: For finding, focusing, and managing Windows windows
-  **pynput**: For global listening and keyboard key management
-  **pyautogui**: For precise simulation of clicks and key presses
-  **pyperclip**: For interacting with the operating system clipboard
