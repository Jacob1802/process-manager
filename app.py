
from tkinter import messagebox, simpledialog
import tkinter as tk
import subprocess
import logging
import ctypes
import utils
import pages
import time
import sys
import os

CONFIG_FILE = "config.json"
LOCKED_FILE = "locked.json"

# Set up logging configuration
logging.basicConfig(
    filename='game_closer.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class ProcessCloserApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Process Closer Service")
        
        # Bring the window to the front
        self.attributes('-topmost', True)
         
        dest_folder = utils.get_dest_folder()
        self.nssm = os.path.join(dest_folder, 'nssm-2.24\\win64\\nssm.exe')
        
        # Set the initial size of the window        
        window_width = 500
        window_height = 500

        # Get the screen's width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the position coordinates for the center of the screen
        position_right = int(screen_width/2 - window_width/2)
        position_down = int(screen_height/2 - window_height/2) - 100
        self.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        self.config = utils.load_config(CONFIG_FILE)
        self.locked_config = utils.load_config(LOCKED_FILE)
        self.frames = {}
        # Create container frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for F in (pages.HomePage, pages.StartServicePage, pages.StopServicePage, pages.DeleteServicePage, pages.LockServicePage, pages.EditServicePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

def run_as_admin():
    if not is_admin():
        script = os.path.abspath(sys.argv[0])
        subprocess.run(['python', 'run_as_admin.py', script] + sys.argv[1:])
        sys.exit()
        
if __name__ == "__main__":
    run_as_admin()

    app = ProcessCloserApp()
    app.mainloop()
