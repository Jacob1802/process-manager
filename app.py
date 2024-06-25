import tkinter as tk
import subprocess
import logging
import ctypes
import utils
import pages
import sys
import os

def get_resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
# TODO: make exe, sign code, make view started/operating processes page

appdata_dir = os.path.join(os.environ['APPDATA'], 'ProcessCloserService')
os.makedirs(appdata_dir, exist_ok=True)
config_dir = os.path.join(appdata_dir, 'config')
os.makedirs(config_dir, exist_ok=True)
log_dir = os.path.join(appdata_dir, 'logs')
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, 'output.log')
logging.basicConfig(filename=log_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class ProcessCloserApp(tk.Tk):
    def __init__(self):
        super().__init__()
        try:
            self.title("Process Closer Service")
            
            # Bring the window to the front
            self.attributes('-topmost', True)
            
            utils.check_and_install_nssm()
            self.nssm = os.path.join(appdata_dir, 'nssm-2.24', 'win64', 'nssm.exe')
            
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

            self.CONFIG_FILE = os.path.join(config_dir, 'config.json')
            self.config = utils.load_config(self.CONFIG_FILE)
            
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
        except Exception as e:
            logging.error(f'app error {e}')
        
        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def move_to_back(self):
        self.attributes('-topmost', False)
        self.lower()

        
if __name__ == "__main__":
    try:
        app = ProcessCloserApp()
        app.mainloop()
    except Exception as e:
        logging.error(f'Unhandled exception: {e}', exc_info=True)
        raise