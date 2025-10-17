import tkinter as tk
from tkinter import messagebox
import time
import pyperclip
import threading
import queue
import pyautogui
from pynput import keyboard
from pywinauto import Desktop, timings
from pywinauto.findwindows import ElementNotFoundError

class AutoPasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoPaster v10.0 (Final)")
        self.root.geometry("450x250")
        self.root.resizable(False, False)

        timings.Timings.fast()

        self.is_running = False
        self.listener_thread = None
        self.manager_thread = None
        
        self.command_queue = queue.Queue()
        self.run_id_counter = 0
        self.active_worker_thread = None
        self.cached_chrome_window = None

        self.current_keys = set()
        self.shortcut_was_fired = False
        self.COMBINATION = set()

        self.title_label = tk.Label(root, text="Target Tab Title:")
        self.title_label.pack(pady=(10, 0))
        self.title_entry = tk.Entry(root, width=60)
        self.title_entry.pack(pady=5)
        self.title_entry.insert(0, "Google Gemini")

        self.shortcut_label = tk.Label(root, text="Shortcut (e.g., f1, ctrl_l + a)")
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
        except Exception:
            error_text = "Invalid Shortcut Format!\n\nUse '+' to combine keys.\nExamples: f1, ctrl_l + c"
            messagebox.showerror("Shortcut Error", error_text)
            return
            
        self.is_running = True
        self.status_label.config(text="Status: Running", fg="green")
        self.start_stop_button.config(text="Stop")
        self.title_entry.config(state='disabled')
        self.shortcut_entry.config(state='disabled')
        self.manager_thread = threading.Thread(target=self.task_manager, args=(target_title,), daemon=True)
        self.manager_thread.start()
        
        if self.listener_thread is None or not self.listener_thread.is_alive():
            self.listener_thread = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
            self.listener_thread.start()

    def stop_listener(self):
        self.is_running = False
        self.command_queue.put('STOP_APP')
        self.status_label.config(text="Status: Stopped", fg="red")
        self.start_stop_button.config(text="Start")
        self.title_entry.config(state='normal')
        self.shortcut_entry.config(state='normal')
        
    def on_closing(self):
        self.is_running = False
        if self.listener_thread and self.listener_thread.is_alive():
            self.listener_thread.stop()
        self.root.destroy()

    def on_press(self, key):
        if not self.is_running: return
        if key in self.COMBINATION:
            self.current_keys.add(key)
            if all(k in self.current_keys for k in self.COMBINATION) and not self.shortcut_was_fired:
                self.command_queue.put('shortcut_pressed')
                self.shortcut_was_fired = True
    
    def on_release(self, key):
        if key in self.COMBINATION:
            self.shortcut_was_fired = False
        self.current_keys.discard(key)

    def task_manager(self, target_title):
        while self.is_running:
            try:
                command = self.command_queue.get(timeout=1)
                if command == 'shortcut_pressed':
                    if self.active_worker_thread and self.active_worker_thread.is_alive():
                        continue
                    self.run_id_counter += 1
                    worker = threading.Thread(target=self.clipboard_worker, args=(self.run_id_counter, pyperclip.paste(), target_title))
                    worker.start()
                    self.active_worker_thread = worker
                elif command == 'STOP_APP': break
            except queue.Empty: continue

    def clipboard_worker(self, worker_run_id, initial_clipboard, target_title):
        for _ in range(50):
            if not self.is_running or worker_run_id != self.run_id_counter:
                return
            
            new_clipboard_content = pyperclip.paste()
            if new_clipboard_content and new_clipboard_content != initial_clipboard:
                self.paste_in_target_tab(new_clipboard_content, target_title)
                return
            time.sleep(0.15)

    def perform_paste_action(self, text_to_paste, target_window):
        try:
            target_window.set_focus()
            client_rect = target_window.client_rect()
            relative_x = client_rect.width() // 2
            relative_y = client_rect.height() - 125
            
            target_window.click_input(coords=(relative_x, relative_y))
            time.sleep(0.1)

            # --- CRITICAL LOGIC FIX ---
            # 1. Go to the absolute end of all text FIRST.
            pyautogui.hotkey('ctrl', 'end')
            time.sleep(0.05) # Brief pause for the cursor to move

            # 2. Press space to add separation.
            pyautogui.press('space')
            
            # 3. Now, perform the paste operation.
            original_clipboard = pyperclip.paste()
            pyperclip.copy(text_to_paste)
            pyautogui.hotkey('ctrl', 'v')
            
            # 4. Restore the original clipboard content.
            pyperclip.copy(original_clipboard)

        except Exception as e:
            error_message = f"An error occurred during paste action:\n{e}"
            self.root.after(0, lambda: messagebox.showerror("Paste Error", error_message))

    def paste_in_target_tab(self, text_to_paste, target_title):
        target_window = None
        target_title_lower = target_title.lower()

        if self.cached_chrome_window:
            try:
                if hasattr(self.cached_chrome_window, 'exists') and self.cached_chrome_window.exists():
                    if self.cached_chrome_window.class_name() == 'Chrome_WidgetWin_1':
                        if target_title_lower in self.cached_chrome_window.window_text().lower():
                            target_window = self.cached_chrome_window
            except Exception:
                 self.cached_chrome_window = None
        
        if not target_window:
            try:
                desktop = Desktop(backend="win32")
                chrome_windows = desktop.windows(class_name="Chrome_WidgetWin_1", top_level_only=True)
                
                if not chrome_windows:
                    self.root.after(0, lambda: messagebox.showerror("Chrome Error", "No Chrome window found."))
                    return
                
                for window in chrome_windows:
                    if window.is_minimized():
                        window.restore()
                        time.sleep(0.2)
                    
                    window.set_focus()
                    
                    initial_title = window.window_text()
                    if target_title_lower in initial_title.lower():
                        target_window = window
                        break
                    
                    for _ in range(30):
                        pyautogui.hotkey('ctrl', 'tab')
                        time.sleep(0.09)
                        current_title = window.window_text()
                        if target_title_lower in current_title.lower():
                            target_window = window
                            break
                        if current_title == initial_title:
                            break
                    if target_window:
                        break
            except Exception as e:
                error_message = f"Error during window search:\n{e}"
                self.root.after(0, lambda: messagebox.showerror("Search Error", error_message))
                return

        if target_window:
            self.cached_chrome_window = target_window
            self.perform_paste_action(text_to_paste, target_window)
        else:
            self.root.after(0, lambda: messagebox.showinfo("Tab Not Found", f"Could not find tab '{target_title}'."))

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoPasterApp(root)
    root.mainloop()