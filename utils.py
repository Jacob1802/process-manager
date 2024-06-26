import subprocess
import requests
import zipfile
import logging
import psutil
import json
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


appdata_dir = os.path.join(os.environ['APPDATA'], 'ProcessCloserService')
zip_path = os.path.join(appdata_dir, 'nssm-2.24.zip')
nssm_path = os.path.join(appdata_dir, "nssm-2.24", "win64", "nssm.exe")
error_log_path = os.path.join(appdata_dir, 'logs', 'output.log')

def check_and_install_nssm():
    """Check if NSSM is installed in System32 and install it if not."""
    if not os.path.exists(nssm_path):
        download_nssm()
        extract_zip(zip_path, appdata_dir)
        os.remove(zip_path)

def download_nssm():
    """Helper function to download a file from a URL to a local path."""
    download_url = "https://nssm.cc/release/nssm-2.24.zip"
    with requests.get(download_url, stream=True) as r:
        r.raise_for_status()
        with open(zip_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def extract_zip(zip_filepath, extract_to):
    """Extract a zip file to a specified directory."""
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def create_service(service_name):
    if not os.path.exists(nssm_path):
        logging.error("Error: NSSM not installed")
        return
    
    process_closer_file = get_resource_path('close.py')
    try:
        # Ensure paths with spaces are properly quoted
        install_command = [nssm_path, 'install', service_name, 'python', process_closer_file, service_name]
        subprocess.run(install_command, check=True, capture_output=True, text=True)

        set_stdout_command = [nssm_path, 'set', service_name, 'AppStdout', error_log_path]
        subprocess.run(set_stdout_command, check=True, capture_output=True, text=True)
        
        set_stderr_command = [nssm_path, 'set', service_name, 'AppStderr', error_log_path]
        subprocess.run(set_stderr_command, check=True, capture_output=True, text=True)
        
        set_env_command = [nssm_path, 'set', service_name, 'AppEnvironmentExtra', f"APPDATA={os.environ['APPDATA']}"]
        subprocess.run(set_env_command, check=True, capture_output=True, text=True)
        
        start_command = [nssm_path, 'start', service_name]
        subprocess.run(start_command, check=True, capture_output=True, text=True)

    except subprocess.CalledProcessError as e:
        logging.error(f"Unexpected error: {e}", exc_info=True)

def restart_service(service_name):
    try:
        subprocess.run([nssm_path, 'restart', service_name], check=True, capture_output=True, text=True)
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}", exc_info=True)

def load_config(config_file):
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return json.load(f)
    return {}

def save_config(config_file, config):
    with open(config_file, "w") as f:
        json.dump(config, f, indent=4)

def convert_days_to_nums(days):
    day_map = {
        'monday' : 0,
        'tuesday' : 1,
        'wednesday' : 2,
        'thursday' : 3,
        'friday' : 4,
        'saturday' : 5,
        'sunday' : 6,
    }
    return [day_map[day] for day in days]

def get_available_processes():
    return {proc.info['name'].lower(): proc for proc in psutil.process_iter(['name']) if '.exe' in proc.info['name'].lower()}