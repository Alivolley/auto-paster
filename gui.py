import tkinter as tk
from tkinter import messagebox
import time
import pyperclip
import threading
import queue
import pyautogui
from pynput import keyboard
from pywinauto import Desktop

class AutoPasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoPaster v1.0")
        self.root.geometry("450x250")
        self.root.resizable(False, False)

        # --- State Variables ---
        self.is_running = False
        self.listener_thread = None
        self.manager_thread = None
        
        # --- Communication & Cache ---
        self.command_queue = queue.Queue()
        self.run_id_counter = 0
        self.active_worker_thread = None
        self.cached_chrome_window = None

        # --- Keyboard Listener State ---
        self.current_keys = set()
        self.shortcut_was_fired = False
        self.COMBINATION = set()

        # --- Create Widgets ---
        self.title_label = tk.Label(root, text="Target Tab Title:")
        self.title_label.pack(pady=(10, 0))
        self.title_entry = tk.Entry(root, width=60)
        self.title_entry.pack(pady=5)
        self.title_entry.insert(0, "ChatGpt")

        self.shortcut_label = tk.Label(root, text="Shortcut (like : f1 , ctrl_l + a  , alt_r + shift)")
        self.shortcut_label.pack(pady=(10, 0))
        self.shortcut_entry = tk.Entry(root, width=60)
        self.shortcut_entry.pack(pady=5)
        self.shortcut_entry.insert(0, "f1")

        self.control_frame = tk.Frame(root)
        self.control_frame.pack(pady=20)
        
        self.start_stop_button = tk.Button(self.control_frame, text="Start", width=15, command=self.toggle_start_stop)
        self.start_stop_button.pack(side=tk.LEFT, padx=10)
        
        self.status_label = tk.Label(self.control_frame, text="Status: Stopped", fg="red")
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    # --- UI Methods ---
    def toggle_start_stop(self):
        if self.is_running: self.stop_listener()
        else: self.start_listener()

    def start_listener(self):
        target_title = self.title_entry.get().strip()
        shortcut_str = self.shortcut_entry.get().strip()
        if not target_title or not shortcut_str:
            messagebox.showerror("Input Error", "Both fields must be filled.")
            return
        try:
            keys = [k.strip() for k in shortcut_str.split('+')]
            self.COMBINATION = set()
            for key in keys:
                if len(key) == 1: self.COMBINATION.add(keyboard.KeyCode.from_char(key))
                else: self.COMBINATION.add(getattr(keyboard.Key, key))
        except Exception as e:
            # --- THIS IS THE MODIFIED PART ---
            error_text = """Invalid Shortcut Format!

Please use the correct format, separating keys with ' + '.
The key names must match the 'pynput' library.

--- EXAMPLES ---
- Single Key:
f1
.

- Modifier + Key:
ctrl_l + c
alt_r + 1

- Multiple Modifiers:
ctrl_l + shift + s
alt_l + shift + f12

--- COMMON KEY NAMES ---
Control: ctrl_l, ctrl_r
Alt: alt_l, alt_r
Shift: shift_l, shift_r
Function Keys: f1, f2, ... , f12
Special Keys: space, enter, esc, backspace
"""
            messagebox.showerror("Shortcut Error", error_text)
            return
        self.is_running = True
        self.status_label.config(text="Status: Running", fg="green")
        self.start_stop_button.config(text="Stop")
        self.title_entry.config(state='disabled')
        self.shortcut_entry.config(state='disabled')
        self.manager_thread = threading.Thread(target=self.task_manager, args=(target_title,), daemon=True)
        self.manager_thread.start()
        self.listener_thread = threading.Thread(target=self.keyboard_listener_thread, daemon=True)
        self.listener_thread.start()
        print("--> Listener started.")

    def stop_listener(self):
        self.is_running = False
        self.command_queue.put('STOP_APP')
        self.status_label.config(text="Status: Stopped", fg="red")
        self.start_stop_button.config(text="Start")
        self.title_entry.config(state='normal')
        self.shortcut_entry.config(state='normal')
        print("--> Stop signal sent.")

    def on_closing(self):
        self.is_running = False
        if self.manager_thread and self.manager_thread.is_alive(): self.manager_thread.join(timeout=0.2)
        if self.listener_thread and self.listener_thread.is_alive(): self.listener_thread.join(timeout=0.2)
        self.root.destroy()

    # --- Core Logic Methods ---
    def keyboard_listener_thread(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            while self.is_running: time.sleep(0.1)
            listener.stop()
    
    def on_press(self, key):
        if not self.is_running or not self.COMBINATION: return
        if key in self.COMBINATION:
            self.current_keys.add(key)
            if all(k in self.current_keys for k in self.COMBINATION) and not self.shortcut_was_fired:
                self.command_queue.put('shortcut_pressed')
                self.shortcut_was_fired = True
    
    def on_release(self, key):
        if not self.is_running: return
        try:
            if key in self.current_keys: self.current_keys.remove(key)
            if key in self.COMBINATION: self.shortcut_was_fired = False
        except KeyError: pass

    def task_manager(self, target_title):
        while self.is_running:
            try:
                command = self.command_queue.get(timeout=1)
                if command == 'shortcut_pressed':
                    if self.active_worker_thread and self.active_worker_thread.is_alive(): pass
                    self.run_id_counter += 1
                    new_id = self.run_id_counter
                    print(f"--> Starting Worker #{new_id}...")
                    initial_content = pyperclip.paste()
                    worker = threading.Thread(target=self.clipboard_worker, args=(new_id, initial_content, target_title))
                    worker.start()
                    self.active_worker_thread = worker
                elif command == 'STOP_APP': break
            except queue.Empty: continue
    
    def clipboard_worker(self, worker_run_id, initial_clipboard, target_title):
        for i in range(int(8 * 5)):
            if not self.is_running or worker_run_id != self.run_id_counter: return
            time.sleep(0.2)
            new_clipboard_content = pyperclip.paste()
            if new_clipboard_content != initial_clipboard and new_clipboard_content:
                print(f"\n--- New text found by Worker #{worker_run_id}! ---")
                self.paste_in_chrome_tab(new_clipboard_content, target_title)
                return
        print(f"--> Worker #{worker_run_id} timed out after 8 seconds.")

    def perform_paste_action(self, text_to_paste):
        pyautogui.press(','); time.sleep(0.1)
        pyautogui.press('backspace'); time.sleep(0.1)
        original_clipboard = pyperclip.paste()
        pyperclip.copy(text_to_paste)
        pyautogui.hotkey('ctrl', 'v'); time.sleep(0.1)
        time.sleep(0.4)
        pyautogui.hotkey('ctrl', 'end')
        pyperclip.copy(original_clipboard)
        print("--> Successfully appended the text and moved to the end.")

    def paste_in_chrome_tab(self, text_to_paste, target_title):
        try:
            target_title_lower = target_title.lower()
            target_window = None
            if self.cached_chrome_window and self.cached_chrome_window.is_visible():
                print("--> Fast Search: Using cached window.")
                target_window = self.cached_chrome_window
            else:
                print(f"--> Full Search: Searching all Chrome windows for tab '{target_title}'...")
                desktop = Desktop(backend="win32")
                chrome_windows = desktop.windows(class_name="Chrome_WidgetWin_1", title_re=".*Chrome.*", top_level_only=True, visible_only=True)
                if not chrome_windows:
                    self.root.after(0, lambda: messagebox.showerror("Chrome Error", "No active Chrome window found at all."))
                    return
                for window in chrome_windows:
                    print(f"--> Checking window: '{window.window_text()}'")
                    window.set_focus(); time.sleep(0.2)
                    initial_title = window.window_text()
                    if target_title_lower in initial_title.lower():
                        self.cached_chrome_window = window; target_window = window; break
                    for i in range(25):
                        pyautogui.hotkey('ctrl', 'tab'); time.sleep(0.15)
                        current_title = window.window_text()
                        if target_title_lower in current_title.lower():
                            self.cached_chrome_window = window; target_window = window; break 
                        if current_title == initial_title: break 
                    if target_window: break 
            if target_window:
                print(f"--> Window found! Focusing tab and pasting...")
                target_window.set_focus()
                for i in range(25):
                    if target_title_lower in target_window.window_text().lower():
                        self.perform_paste_action(text_to_paste)
                        return
                    pyautogui.hotkey('ctrl', 'tab')
                    time.sleep(0.1)
            self.root.after(0, lambda title=target_title: messagebox.showerror("Chrome Error", f"Could not find tab '{title}' in any open Chrome window."))
        except Exception as e:
            self.root.after(0, lambda err=e: messagebox.showerror("Unexpected Error", f"An unexpected error occurred:\n{err}"))

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoPasterApp(root)
    root.mainloop()