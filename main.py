
import tkinter as tk
import time
import ctypes
import threading
from PIL import Image, ImageTk
import keyboard

running = True

def move_image_horizontally(window, label, screen_width, screen_height, speed=5, delay=0.01):
    """Moves the image horizontally across the bottom of the screen."""
    global running
    window.deiconify()
    y_position = screen_height - 100
    for x_position in range(0, screen_width, speed):
        if not running:  # Stop if running is set to False
            break
        window.geometry(f"100x100+{x_position}+{y_position}")
        ensure_on_top(window)  # Ensure the window stays above the taskbar
        window.update()
        time.sleep(delay)
    window.withdraw()

def ensure_on_top(window):
    """Ensure the window stays on top of the taskbar."""
    hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
    ctypes.windll.user32.SetWindowPos(
        hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002  # HWND_TOPMOST | SWP_NOMOVE | SWP_NOSIZE
    )

def make_window_invisible(window):
    """Make the tkinter window invisible in the taskbar."""
    hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
    style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
    style = style & ~0x00000080 | 0x00000008  # Remove WS_EX_APPWINDOW, add WS_EX_TOOLWINDOW
    ctypes.windll.user32.SetWindowLongW(hwnd, -20, style)

def stop_script():
    """Set the running flag to False to stop the script."""
    global running
    running = False

def listen_for_stop():
    """Listen for the Ctrl + P key combination to stop the script."""
    global running
    keyboard.wait("ctrl+p")
    stop_script()

def main():
    global running

    root = tk.Tk()
    root.overrideredirect(True)  # Remove window decorations
    root.attributes("-topmost", True)  # Keep the window on top
    root.config(bg="black")

    # Make the window invisible in the taskbar
    make_window_invisible(root)

    # Load and set up the image
    img = Image.open("hobbes.png").convert("RGBA")  # Ensure the image has transparency
    img = img.resize((100, 100), Image.Resampling.LANCZOS)
    tk_img = ImageTk.PhotoImage(img)

    label = tk.Label(root, image=tk_img, bg="black", borderwidth=0, highlightthickness=0)
    label.pack()

    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Start the key listener in a separate thread
    stop_thread = threading.Thread(target=listen_for_stop, daemon=True)
    stop_thread.start()

    # Move the image horizontally
    try:
        while running:
            move_image_horizontally(root, label, screen_width, screen_height, speed=10, delay=0.01)
            time.sleep(3600)  # Pause for 5 seconds before moving again
    except KeyboardInterrupt:
        pass
    finally:
        root.destroy()

if __name__ == "__main__":
    main()
