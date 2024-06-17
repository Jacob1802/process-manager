import tkinter as tk
import subprocess
import utils
import logging
import sys

logging.basicConfig(
    filename='game_closer.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

CONFIG_FILE = 'config.json'

class BasePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # self.config = utils.load_config(CONFIG_FILE)
        self.controller = controller

        # Configure the grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_rowconfigure(8, weight=1)
        self.grid_rowconfigure(9, weight=1)
        self.grid_rowconfigure(10, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Add padding to the top by configuring an empty row at the top
        self.grid_rowconfigure(0, minsize=10)
    
    def add_service_page_header(self, text):
        tk.Label(self, text=text).grid(row=0, column=1, columnspan=2, pady=10)

    def add_service_name_input(self):
        tk.Label(self, text="Service Name:").grid(row=1, column=1, pady=0, sticky="e")
        self.service_name_entry = tk.Entry(self)
        self.service_name_entry.grid(row=1, column=2, pady=0, sticky="w")

    def add_submit(self, command):
        self.submit_button = tk.Button(self, text="Submit", command=command)
        self.submit_button.grid(row=5, column=1, columnspan=2, pady=20)

    def add_back_to_home_button(self):
        tk.Button(self, text="Back to Home", command=lambda: self.controller.show_frame("HomePage")).grid(row=10, column=1, columnspan=2, pady=10)

class HomePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        button_width = 30  # Set a standard width for all buttons

        self.display_potential_services_button = tk.Button(self, text="Display Potential Processes", command=self.display_potential_services, width=button_width)
        self.display_potential_services_button.grid(row=1, column=1, pady=10)
        
        tk.Button(self, text="Set Up Process Closure Schedule", command=lambda: controller.show_frame("StartServicePage"), width=button_width).grid(row=2, column=1, pady=10)
        tk.Button(self, text="Stop A Process Closure Schedule", command=lambda: controller.show_frame("StopServicePage"), width=button_width).grid(row=3, column=1, pady=10)
        tk.Button(self, text="Delete A Process Closure Schedule", command=lambda: controller.show_frame("DeleteServicePage"), width=button_width).grid(row=4, column=1, pady=10)
        tk.Button(self, text="Lock A Process Closure Schedule", command=lambda: controller.show_frame("LockServicePage"), width=button_width).grid(row=5, column=1, pady=10)
        tk.Button(self, text="Edit A Process Closure Schedule", command=lambda: controller.show_frame("EditServicePage"), width=button_width).grid(row=6, column=1, pady=10)

    def display_potential_services(self):
        running_processes = utils.get_available_processes()
        sorted_processes = sorted(running_processes.keys())

        process_list_window = tk.Toplevel(self)
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
            tk.Label(scrollable_frame, text=f"• {process}", anchor='w', justify='left').pack(anchor='w', padx=10, pady=2)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
class StartServicePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # Configure the grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_rowconfigure(8, weight=1)
        self.grid_rowconfigure(9, weight=1)
        self.grid_rowconfigure(10, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        # Add the widgets using grid
        self.add_service_page_header(text="Start Service Page")
        self.add_service_name_input()

        self.start_time_label = tk.Label(self, text="Start Time (HH:MM):")
        self.start_time_label.grid(row=2, column=1, pady=0, sticky="e")

        self.start_time_entry = tk.Entry(self)
        self.start_time_entry.grid(row=2, column=2, pady=0, sticky="w")

        self.end_time_label = tk.Label(self, text="End Time (HH:MM):")
        self.end_time_label.grid(row=3, column=1, pady=0, sticky="e")

        self.end_time_entry = tk.Entry(self)
        self.end_time_entry.grid(row=3, column=2, pady=0, sticky="w")

        self.days_label = tk.Label(self, text="Days (e.g. Monday, Tuesday, Sunday):")
        self.days_label.grid(row=4, column=1, pady=0, sticky="e")

        self.days_entry = tk.Entry(self)
        self.days_entry.grid(row=4, column=2, pady=0, sticky="w")

        self.add_submit(self.name_service)
        self.add_back_to_home_button()
    
    def name_service(self):
        service_name = self.service_name_entry.get()
        start_time = self.start_time_entry.get()
        end_time = self.end_time_entry.get()
        days = self.days_entry.get()
        
        # Here you can add the logic to handle the form submission
        # For example, saving the data to a config file, validating input, etc.
        if service_name and start_time and end_time and days:
            self.start_service_logic(service_name, start_time, end_time, days)
            self.controller.show_frame("HomePage")
        else:
            tk.messagebox.showerror("Error", "All fields are required!")

    def start_service_logic(self, service_name, start_time, end_time, days):
        try:
            if not service_name:
                tk.messagebox.showerror("Error", "Service name cannot be empty")
                return

            if service_name in self.controller.config.keys():
                tk.messagebox.showerror("Error", "Service already exists")
                return

            if not self.check_time_entry(start_time):
                return
            if not self.check_time_entry(end_time):
                return
            day_list = self.check_day_entry(days)
            if not day_list:
                return

            self.controller.config[service_name] = {
                "start_time": start_time,
                "end_time": end_time,
                "days": day_list
            }

            utils.save_config(CONFIG_FILE, self.controller.config)
            utils.create_service(service_name, sys.executable)
            tk.messagebox.showinfo("Info", "Service started successfully")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to start service: {e}")

    def check_time_entry(self, time):
        if ":" not in time:
            tk.messagebox.showerror("Error", "Missing semi colon")
            return False
        time_str = time.split(':')
        if not time_str[0].isnumeric() or not time_str[1].isnumeric():
            tk.messagebox.showerror("Error", "Invalid time")
            return False

        return True

    def check_day_entry(self, days_string):
        days = []
        for day in days_string.split(','):
            if day.strip().lower() not in ['monday', 'tuesday', 'wednesday', 'thrusday', 'friday', 'saturday', 'sunday']:
                tk.messagebox.showerror("Error", "Invalid day")
                return
            else: days.append(day)
        
        return days

class StopServicePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.add_service_page_header(text="Stop Service Page")
        self.add_service_name_input()
        self.add_submit(self.stop_service)
        self.add_back_to_home_button()
        
    def stop_service(self):
        service_name = self.service_name_entry.get()
        
        if not service_name:
            tk.messagebox.showerror("Error", "Service name cannot be empty")
            return

        if service_name not in self.controller.config.keys():
            tk.messagebox.showerror("Error", "Service does not exist")
            return

        try:
            subprocess.run([self.controller.nssm, 'stop', service_name], check=True)
            tk.messagebox.showinfo("Info", "Service stopped successfully")
            self.controller.show_frame("HomePage")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to stop service: {e}")

class DeleteServicePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.add_service_page_header(text="Delete Service Page")
        self.add_service_name_input()
        self.add_submit(self.delete_service)
        self.add_back_to_home_button()
        
    def delete_service(self):
        service_name = self.service_name_entry.get()
        
        if not service_name:
            tk.messagebox.showerror("Error", "Service name cannot be empty")
            return
    
        if service_name not in self.controller.config.keys():
            tk.messagebox.showerror("Error", "Service does not exist")
            return
    
        try:
            subprocess.run([self.controller.nssm, 'remove', service_name])
            del self.controller.config[service_name]
            utils.save_config(CONFIG_FILE, self.controller.config)
            tk.messagebox.showinfo("Info", "Service Deleted successfully")
            self.controller.show_frame("HomePage")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to Delete service: {e}")

class LockServicePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.add_service_page_header(text="Lock Service Page")
        self.add_service_name_input()
        self.add_back_to_home_button()

class EditServicePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.add_service_page_header(text="Edit Service Page")
        self.add_service_name_input()
        self.add_back_to_home_button()