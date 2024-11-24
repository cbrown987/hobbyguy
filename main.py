import tkinter as tk
from PIL import Image, ImageTk
import time
import ctypes

def move_image_horizontally(window, label, screen_width, screen_height, speed=5, delay=0.01):
    """Moves the image horizontally across the bottom of the screen."""
    y_position = screen_height - 100
    for x_position in range(0, screen_width, speed):
        window.geometry(f"100x100+{x_position}+{y_position}")
        window.update()
        time.sleep(delay)

def make_window_invisible(window):
    """Make the tkinter window invisible in the taskbar."""
    hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
    ctypes.windll.user32.SetWindowLongW(hwnd, -20,
        ctypes.windll.user32.GetWindowLongW(hwnd, -20) | 0x00000080)  # WS_EX_TOOLWINDOW
    ctypes.windll.user32.ShowWindow(hwnd, 0)  # Hide window initially

def main():
    root = tk.Tk()
    root.overrideredirect(True)  # Remove window decorations
    root.attributes("-topmost", True)  # Keep the window on top
    root.config(bg="black")

    # Make the window invisible in taskbar
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

    # Move the image horizontally with a pause after each run
    try:
        while True:
            move_image_horizontally(root, label, screen_width, screen_height, speed=10, delay=0.01)
            time.sleep(3600)  # Pause for 1 hour
    except KeyboardInterrupt:
        root.destroy()

if __name__ == "__main__":
    main()
