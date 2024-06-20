from tkinter import messagebox
import datetime as dt
import tkinter as tk
import subprocess
import logging
import utils

class BasePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
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
    
    def start_service_logic(self, service_name, start_time, end_time, days):
        try:
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
                "days": day_list,
                'status': 'running'
            }

            utils.save_config(self.controller.CONFIG_FILE, self.controller.config)
            utils.create_service(service_name)
            messagebox.showinfo("Info", "Service started successfully")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start service: {e}")

    def check_time_entry(self, time):
        if ":" not in time:
            messagebox.showerror("Error", "Missing semi colon")
            return False
        time_str = time.split(':')
        if not time_str[0].isnumeric() or not time_str[1].isnumeric() or len(time) != 5:
            messagebox.showerror("Error", "Invalid time")
            return False

        return True

    def check_day_entry(self, days_string):
        days = []
        for day in days_string.split(','):
            if day.strip().lower() not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                messagebox.showerror("Error", "Invalid day")
                return
            else: days.append(day)
        
        return days

    def validate_service_name(self, service_name):
        if not service_name:
            messagebox.showerror("Error", "Service name cannot be empty")
            return False
    
        if service_name not in self.controller.config.keys():
            messagebox.showerror("Error", "Service does not exist")
            return False
        
        if service_name in self.controller.locked_config.keys():
            # Calculate time left, if time left throw error
            if remaining_time := self.calculate_remaining_time(service_name):
                messagebox.showerror("Error", f"Service is locked for {remaining_time[0]} hours and {remaining_time[1]} more minutes")
                return False
        
        return True

    def add_service_name_input(self):
        tk.Label(self, text="Service Name:").grid(row=1, column=1, pady=0, sticky="e")
        self.service_name_entry = tk.Entry(self)
        self.service_name_entry.grid(row=1, column=2, pady=0, sticky="w")

    def add_submit(self, command):
        self.submit_button = tk.Button(self, text="Submit", command=command)
        self.submit_button.grid(row=5, column=1, columnspan=2, pady=20)

    def add_back_to_home_button(self):
        tk.Button(self, text="Back to Home", command=lambda: self.controller.show_frame("HomePage")).grid(row=10, column=1, columnspan=2, pady=10)
    
    def check_if_service_locked(self, service_name):
        start_lock = self.controller.locked_config[service_name]['start_time']
        duration = self.controller.locked_config[service_name]['length_seconds']

        return True if (start_lock + duration) > dt.datetime.now().timestamp() else False 

    def calculate_remaining_time(self, service_name):
        if self.check_if_service_locked(service_name):
            start_time = self.controller.locked_config[service_name]['start_time']
            duration = self.controller.locked_config[service_name]['length_seconds']
            remaining_time = ((start_time + duration) - dt.datetime.now().timestamp()) / 60 / 60
            hours = int(remaining_time)
            minutes = (remaining_time - hours) * 60
            minutes = round(minutes) 
            return (hours, minutes)
        # Release lock
        del self.controller.locked_config[service_name]
        return None
    
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

        # Add to the grid layout
        self.grid_columnconfigure(3, weight=1)

        # Add the widgets using grid
        tk.Label(self, text="Start Service Page").grid(row=0, column=1, columnspan=2, pady=10)
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

        self.add_submit(self.start_service)
        self.add_back_to_home_button()
    
    def start_service(self):
        try:
            service_name = self.service_name_entry.get()

            if service_name in self.controller.config.keys():
                messagebox.showerror("Error", "Service already exists")
                return
            
            start_time = self.start_time_entry.get()
            end_time = self.end_time_entry.get()
            days = self.days_entry.get()
            
            if start_time and end_time and days:
                result = self.start_service_logic(service_name, start_time, end_time, days)
                if result:
                    self.controller.show_frame("HomePage")
            else:
                messagebox.showerror("Error", "All fields are required!")
        except Exception as e:
            logging.error(e)

class StopServicePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.grid_rowconfigure(0, minsize=20)

        # Adjust column configurations for better centering
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        tk.Label(self, text="Stop Service Page").grid(row=0, column=1, columnspan=2, pady=10, sticky='n')
        self.add_service_name_input()
        self.add_submit(self.stop_service)
        self.add_back_to_home_button()
        
    def stop_service(self):
        service_name = self.service_name_entry.get()
        if not self.validate_service_name(service_name):
            return

        try:
            subprocess.run([self.controller.nssm, 'stop', service_name], check=True)
            self.controller.config[service_name]['status'] = 'stopped'
            messagebox.showinfo("Info", "Service stopped successfully")
            self.controller.show_frame("HomePage")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop service: {e}")

class DeleteServicePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.grid_rowconfigure(0, minsize=20)

        # Adjust column configurations for better centering
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        tk.Label(self, text="Delete Service Page").grid(row=0, column=1, columnspan=2, pady=10, sticky='n')
        self.add_service_name_input()
        self.add_submit(self.delete_service)
        self.add_back_to_home_button()
        
    def delete_service(self):
        service_name = self.service_name_entry.get()
        if not self.validate_service_name(service_name):
            return
        if self.controller.config[service_name]['status'] != 'stopped':
            messagebox.showerror("Error", "Service must be stopped before it is deleted")
            return

        try:
            self.controller.move_to_back()
            subprocess.run([self.controller.nssm, 'remove', service_name])
            del self.controller.config[service_name]
            utils.save_config(self.controller.CONFIG_FILE, self.controller.config)
            self.controller.attributes('-topmost', True)
            self.controller.show_frame("HomePage")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to Delete service: {e}")

class LockServicePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.grid_rowconfigure(0, minsize=20)

        # Adjust column configurations for better centering
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        
        tk.Label(self, text="Lock Service Page").grid(row=0, column=1, columnspan=2, pady=10, sticky='n')
        self.add_service_name_input()
        self.length_label = tk.Label(self, text="Length (Hrs):")
        self.length_label.grid(row=2, column=1, pady=0, sticky="e")

        self.length_entry = tk.Entry(self)
        self.length_entry.grid(row=2, column=2, pady=0, sticky="w")
        self.add_submit(self.lock_service)
        self.add_back_to_home_button()

    def lock_service(self):
        service_name = self.service_name_entry.get()
        if not self.validate_service_name(service_name):
            return
        
        length = self.length_entry.get()
        # Check if length is valid
        if not length.isnumeric():
            messagebox.showerror("Error", "Invalid time")

        self.controller.locked_config[service_name] = {
            "start_time": dt.datetime.now().timestamp(),
            "length_seconds": int(length) * 60 * 60
        }
        utils.save_config(self.controller.LOCKED_CONFIG, self.controller.locked_config)
        messagebox.showinfo("Info", f"Service successfully locked for {length} hours")
        self.controller.show_frame("HomePage")

class EditServicePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.grid_rowconfigure(0, minsize=20)

        # Adjust column configurations for better centering
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        tk.Label(self, text="Edit Service Page").grid(row=0, column=1, columnspan=2, pady=10, sticky='n')
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

        self.add_submit(self.edit_service_process)
        self.add_back_to_home_button()
    
    def edit_service_process(self):
        service_name = self.service_name_entry.get()
        if not self.validate_service_name(service_name):
            return
        
        start_time = self.start_time_entry.get()
        end_time = self.end_time_entry.get()
        days = self.days_entry.get()
        
        if start_time and end_time and days:
            result = self.start_service_logic(service_name, start_time, end_time, days)
            if result:
                self.controller.show_frame("HomePage")
        else:
            messagebox.showerror("Error", "All fields are required!")