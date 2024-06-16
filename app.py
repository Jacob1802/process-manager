
from tkinter import messagebox, simpledialog
import tkinter as tk
import subprocess
import logging
import ctypes
import utils
import time
import sys
import os

CONFIG_FILE = "config.json"

# Set up logging configuration
logging.basicConfig(
    filename='game_closer.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class ProcessCloserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Closer Service")
        
        # Bring the window to the front
        self.root.attributes('-topmost', True)
        # self.root.after_idle(self.root.attributes, '-topmost', False)

        # Set the initial size of the window
        window_width = 400
        window_height = 400

        # Get the screen's width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the position coordinates for the center of the screen
        position_right = int(screen_width/2 - window_width/2)
        position_down = int(screen_height/2 - window_height/2) - 100
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        logging.info("Initializing ProcessCloserApp")

        self.config = utils.load_config(CONFIG_FILE)

        # self.status_label = tk.Label(root, text="Status: Unknown")
        # self.status_label.pack(pady=10)
        
        button_width = 20  # Set a standard width for all buttons

        self.start_button = tk.Button(root, text="Start A Service", command=self.start_service, width=button_width)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop A Service", command=self.stop_service, width=button_width)
        self.stop_button.pack(pady=10)

        self.remove_button = tk.Button(root, text="Delete A Service", command=self.delete_service, width=button_width)
        self.remove_button.pack(pady=10)

        self.display_potential_services_button = tk.Button(root, text="Display Potential Services", command=self.display_potential_services, width=button_width)
        self.display_potential_services_button.pack(pady=10)

        self.display_locked_services_button = tk.Button(root, text="Display Stopped Services", command=self.display_stopped_services, width=button_width)
        self.display_locked_services_button.pack(pady=10)

        self.display_locked_services_button = tk.Button(root, text="Lock A Service", command=self.lock_service, width=button_width)
        self.display_locked_services_button.pack(pady=10)

        self.display_locked_services_button = tk.Button(root, text="Display Locked Services", command=self.display_locked_services, width=button_width)
        self.display_locked_services_button.pack(pady=10)

        # self.update_status()
        dest_folder = utils.get_dest_folder()
        self.nssm = os.path.join(dest_folder, 'nssm-2.24\\win64\\nssm.exe')

    # def update_status(self):
    #     service_name = self.get_service_name()
    #     if service_name and is_gamecloser_running(service_name):
    #         self.status_label.config(text="Status: Running")
    #     else:
    #         self.status_label.config(text="Status: Stopped")
    #     self.root.after(10000, self.update_status)  # Update status every 10 seconds
    
    # def get_service_name(self):
    #     return self.root.title() if self.root.title() != "Game Closer Service" else None
    
    def start_service(self):
        logging.info("Attempting to start service")
        self.root.attributes('-topmost', False)
        
        service_name = simpledialog.askstring("Input", "Enter service name:")
        
        if not service_name:
            messagebox.showerror("Error", "Service name cannot be empty")
            return

        if service_name in self.config.keys():
            messagebox.showerror("Error", "Service already exists")
            return
        
        try:
            start_time = simpledialog.askstring("Input", "Enter start time (HH:MM)(24hr time):")
            if not self.check_time_entry(start_time): return

            end_time = simpledialog.askstring("Input", "Enter end time (HH:MM)(24hr time):")
            if not self.check_time_entry(end_time): return

            days_string = simpledialog.askstring("Input", "Enter days (Monday-Sunday, comma separated, e.g., Monday,Tuesday,Saturday,Sunday):")
            days = self.check_day_entry(days_string)
            logging.info(days)
            if not days: return

            self.config[service_name] = {
                "start_time": start_time,
                "end_time": end_time,
                "days": days
            }

            utils.save_config(CONFIG_FILE, self.config)
            utils.create_service(service_name, sys.executable)
            
            messagebox.showinfo("Info", "Service started successfully")
            # self.root.title(service_name)
        except Exception as e:
            logging.error(f"Failed to start service: {e}")
            messagebox.showerror("Error", f"Failed to start service: {e}")

    def check_time_entry(self, time):
        if ":" not in time:
            messagebox.showerror("Error", "Missing semi colon")
            return False
        time_str = time.split(':')
        if not time_str[0].isnumeric() or not time_str[1].isnumeric():
            messagebox.showerror("Error", "Invalid time")
            return False

        return True

    def check_day_entry(self, days_string):
        days = []
        for day in days_string.split(','):
            if day.strip().lower() not in ['monday', 'tuesday', 'wednesday', 'thrusday', 'friday', 'saturday', 'sunday']:
                messagebox.showerror("Error", "Invalid day")
                return
            else: days.append(day)
        
        return days

    def stop_service(self):
        logging.info("Attempting to stop service")
        self.root.attributes('-topmost', False)

        service_name = simpledialog.askstring("Input", "Enter service name:")
        
        if not service_name:
            messagebox.showerror("Error", "Service name cannot be empty")
            return

        if service_name not in self.config.keys():
            messagebox.showerror("Error", "Service does not exist")
            return

        try:
            subprocess.run([self.nssm, 'stop', service_name], check=True)
            messagebox.showinfo("Info", "Service stopped successfully")
            self.root.title("Game Closer Service")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop service: {e}")

    def delete_service(self):
        logging.info("Attempting to delete service")
        self.root.attributes('-topmost', False)

        service_name = simpledialog.askstring("Input", "Enter service name:")
        
        if not service_name:
            messagebox.showerror("Error", "Service name cannot be empty")
            return
    
        if service_name not in self.config.keys():
            messagebox.showerror("Error", "Service does not exist")
            return
    
        try:
            subprocess.run([self.nssm, 'remove', service_name])
            del self.config[service_name]
            utils.save_config(CONFIG_FILE, self.config)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to Delete service: {e}")

    def lock_service(self):
        pass

    def display_potential_services(self):
        self.root.attributes('-topmost', False)
        
        running_processes = utils.get_availavle_processes()
        sorted_processes = sorted(running_processes.keys())

        process_list_window = tk.Toplevel(self.root)
        process_list_window.title("Running Processes")

        canvas = tk.Canvas(process_list_window)
        scrollbar = tk.Scrollbar(process_list_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for process in sorted_processes:
            tk.Label(scrollable_frame, text=f"• Name: {process}", anchor='w', justify='left').pack(anchor='w', padx=10, pady=2)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def display_stopped_services(self):
        self.root.attributes('-topmost', False)

        config = utils.load_config(CONFIG_FILE)

        stopped_processes_window = tk.Toplevel(self.root)
        stopped_processes_window.title("Stopped Processes")

        # Create a new frame within the stopped_processes_window
        frame = tk.Frame(stopped_processes_window)
        frame.pack(fill="both", expand=True)

        for process, process_config in config.items():
            tk.Label(frame, text=f"• Name: {process.title()} | Start time: {process_config['start_time']} | End time: {process_config['end_time']} | Days: {','.join(process_config['days']).title()}", anchor='w', justify='left').pack(anchor='w', padx=10, pady=2)

    def display_locked_services(self):
        self.root.attributes('-topmost', False)
        # Implementation to display locked services
        pass

    def get_service_name(self):
        service_name = simpledialog.askstring("Input", "Enter service name:")
        
        if not service_name:
            messagebox.showerror("Error", "Service name cannot be empty")
            return

        return service_name

    def set_time_days(self):
        logging.info("Setting time and days")
        try:
            start_time = simpledialog.askstring("Input", "Enter start time (HH:MM):")
            end_time = simpledialog.askstring("Input", "Enter end time (HH:MM):")
            days = simpledialog.askstring("Input", "Enter days (0-6, comma separated, e.g., 0,1,2,3):")

            with open("config.json", "w") as f:
                f.write(f"{start_time}\n")
                f.write(f"{end_time}\n")
                f.write(f"{days}\n")

            messagebox.showinfo("Info", "Time and days set successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set time and days: {e}")

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
    root = tk.Tk()
    app = ProcessCloserApp(root)
    root.mainloop()
