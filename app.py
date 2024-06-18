import tkinter as tk
import subprocess
import ctypes
import utils
import pages
import sys
import os


appdata_dir = os.path.join(os.environ['APPDATA'], 'ProcessCloserService')
os.makedirs(appdata_dir, exist_ok=True)

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
        
        self.config_path = os.path.join(appdata_dir, "config.json")
        self.locked_config_path = os.path.join(appdata_dir, "locked.json")

        self.config = utils.load_config(self.config_path)
        self.locked_config = utils.load_config(self.locked_config_path)
        
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