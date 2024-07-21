import os
import subprocess
import sys
import time
import threading
import ctypes
import keyboard
def install_dependencies():
    try:
        import pyautogui
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui"])
    
    try:
        import keyboard
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "keyboard"])
install_dependencies()
user32 = ctypes.windll.user32

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
click_rate = 34
macro_running = False
def get_mouse_position():
    point = ctypes.wintypes.POINT()
    user32.GetCursorPos(ctypes.byref(point))
    return point.x, point.y
def click_current_position():
    while macro_running:
        x, y = get_mouse_position()
        user32.mouse_event(MOUSEEVENTF_LEFTDOWN | MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        # Time interval to control the click rate
        time.sleep(1 / click_rate)
def start_macro():
    global macro_running
    if not macro_running:
        print("Starting macro...")
        macro_running = True
        threading.Thread(target=click_current_position).start()
def stop_macro():
    global macro_running
    if macro_running:
        print("Stopping macro...")
        macro_running = False
def increase_click_rate():
    global click_rate
    click_rate += 1
    print(f"Click rate increased to {click_rate} clicks per second")
def decrease_click_rate():
    global click_rate
    if click_rate > 1:
        click_rate -= 1
        print(f"Click rate decreased to {click_rate} clicks per second")
def check_esc():
    while True:
        if keyboard.is_pressed('Esc'):
            print("Exiting program...")
            stop_macro()
            exit()
        time.sleep(0.1)
keyboard.add_hotkey('F9', start_macro)
keyboard.add_hotkey('F8', stop_macro)
keyboard.add_hotkey('F7', increase_click_rate)
keyboard.add_hotkey('F6', decrease_click_rate)
threading.Thread(target=check_esc).start()
while True:
    time.sleep(0.1)  # Small pause to reduce CPU usage
