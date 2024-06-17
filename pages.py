import tkinter as tk

class BasePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

class HomePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        button_width = 30  # Set a standard width for all buttons
        
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

        self.display_potential_services_button = tk.Button(self, text="Display Potential Processes", command=controller.display_potential_services, width=button_width)
        self.display_potential_services_button.grid(row=1, column=1, pady=10)
        
        tk.Button(self, text="Set Up Process Closure Schedule", command=lambda: controller.show_frame("StartServicePage"), width=button_width).grid(row=2, column=1, pady=10)
        tk.Button(self, text="Stop A Process Closure Schedule", command=lambda: controller.show_frame("StopServicePage"), width=button_width).grid(row=3, column=1, pady=10)
        tk.Button(self, text="Delete A Process Closure Schedule", command=lambda: controller.show_frame("DeleteServicePage"), width=button_width).grid(row=4, column=1, pady=10)
        tk.Button(self, text="Lock A Process Closure Schedule", command=lambda: controller.show_frame("LockServicePage"), width=button_width).grid(row=5, column=1, pady=10)
        tk.Button(self, text="Edit A Process Closure Schedule", command=lambda: controller.show_frame("EditServicePage"), width=button_width).grid(row=6, column=1, pady=10)

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
        tk.Label(self, text="Start Service Page").grid(row=0, column=1, columnspan=2, pady=10)

        self.service_name_label = tk.Label(self, text="Service Name:")
        self.service_name_label.grid(row=1, column=1, pady=0, sticky="e")

        self.service_name_entry = tk.Entry(self)
        self.service_name_entry.grid(row=1, column=2, pady=0, sticky="w")

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

        self.submit_button = tk.Button(self, text="Submit", command=self.submit_service)
        self.submit_button.grid(row=5, column=1, columnspan=2, pady=20)

        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage")).grid(row=6, column=1, columnspan=2, pady=10)
    
    
    def submit_service(self):
        service_name = self.service_name_entry.get()
        start_time = self.start_time_entry.get()
        end_time = self.end_time_entry.get()
        days = self.days_entry.get()
        
        # Here you can add the logic to handle the form submission
        # For example, saving the data to a config file, validating input, etc.
        if service_name and start_time and end_time and days:
            print(f"Service Name: {service_name}")
            print(f"Start Time: {start_time}")
            print(f"End Time: {end_time}")
            print(f"Days: {days}")
            
            # You can call a method from the controller to handle the data
            self.controller.start_service_logic(service_name, start_time, end_time, days)
        else:
            messagebox.showerror("Error", "All fields are required!")

class StopServicePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Label(self, text="Stop Service Page").pack(pady=10)
        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage")).pack()

class DeleteServicePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Label(self, text="Delete Service Page").pack(pady=10)
        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage")).pack()

class LockServicePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Label(self, text="Lock Service Page").pack(pady=10)
        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage")).pack()
