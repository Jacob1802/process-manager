# Process Closer Service

## Overview
Process Closer Service is a process management tool designed to help you manage processes on your system. You can schedule processes to be closed on specific days and between certain hours, or lock a process for a specified number of hours.

**Note: This application is intended for Windows users.**

## Features
- Schedule process closure on specific days and hours.
- Lock a process for a specified duration.
- View and manage running processes.
- Easy-to-use GUI built with Tkinter.

## Installation
### Option 1: Download the Executable
1. **Download the Executable:**
   - [Download Process Closer Service](https://github.com/Jacob1802/process-manager/releases/download/v1.0/ProcessCloserService.exe)

2. **Run the Executable:**
   - Right-click the downloaded executable and run as admin to start the application.

### Option 2: Clone the Repository
1. **Clone the Repository:**
```bash
   - git clone https://github.com/Jacob1802/process-manager.git
   - cd process-manager
   - pip install -r requirements.txt
   - runas /user:Administrator "python app.py"
```

### Option 3: Clone the Repository
1. **Compile the Executable:**
```bash
   - git clone https://github.com/Jacob1802/process-manager.git
   - cd process-manager
   - pip install pyinstaller
   - pyinstaller app.spec
```
navigate to the 'dist' directory then right click and run the file as admin

## Usage
### Main Interface
- **Display Potential Processes:** Shows a list of all currently running processes.
- **Set Up Process Closure Schedule:** Schedule a process to be closed at specific times and days.
- **Stop a Process Closure Schedule:** Stop an existing process closure schedule.
- **Delete a Process Closure Schedule:** Delete a process closure schedule.
- **Lock a Process Closure Schedule:** Lock a process for a specified number of hours.
- **Edit a Process Closure Schedule:** Edit an existing process closure schedule.

### How to Schedule a Process
1. Click on **Set Up Process Closure Schedule**.
2. Enter the process name (without the .exe extension).
3. Enter the start time and end time in HH:MM format.
4. Enter the days of the week (e.g., Monday, Tuesday).
5. Click **Submit**.

### How to Lock a Process
1. Click on **Lock a Process Closure Schedule**.
2. Enter the process name.
3. Enter the number of hours to lock the process.
4. Click **Submit**.


## Technical Details
### `app.py`
This is the main application file that sets up the GUI and handles the main functionalities of the application. It initializes the `ProcessCloserApp` class which sets up the main window and frames for different functionalities.

### `pages.py`
Contains the different pages for the application, such as the home page, start service page, stop service page, delete service page, lock service page, and edit service page. Each page extends the `BasePage` class which provides common functionalities.

### `utils.py`
Utility functions to download and install NSSM, create and manage services, load and save configuration, and get available processes.

### `close.py`
The script responsible for terminating the processes as per the scheduled configuration. It runs as a service managed by NSSM.

## Logging
Logs are stored in the `logs` directory inside the application data directory (`APPDATA/ProcessCloserService`). The main log file is `output.log`.

## Configuration
Configuration is stored in a JSON file located in the `config` directory inside the application data directory (`APPDATA/ProcessCloserService`). The configuration file name is `config.json`.
