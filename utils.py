import subprocess
import requests
import zipfile
import logging
import psutil
import json
import os

appdata_dir = os.path.join(os.environ['APPDATA'], 'ProcessCloserService')
zip_path = os.path.join(appdata_dir, 'nssm-2.24.zip')
nssm_path = os.path.join(appdata_dir, 'nssm-2.24', 'win64', 'nssm.exe')
log_path = os.path.join(appdata_dir, 'output.log')


logging.basicConfig(filename=log_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def check_and_install_nssm():
    """Check if NSSM is installed in System32 and install it if not."""
    if not os.path.exists(nssm_path):
        download_nssm()
        extract_zip(zip_path, appdata_dir)
        # Remove the downloaded zip file after extraction
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


def create_service(service_name, executable):
    if not nssm_path:
        logging.error("Error: Path to NSSM not provided.")
        return
    
    exe_path = 'C:\\Users\\user\\Documents\\Projects\\process-manager\\close.py'

    try:
        subprocess.run([nssm_path, 'install', service_name, executable, exe_path, service_name])
        subprocess.run([nssm_path, 'set', service_name, 'AppStdout', log_path], check=True)
        subprocess.run([nssm_path, 'set', service_name, 'AppStderr', log_path], check=True)
        subprocess.run([nssm_path, 'start', service_name], check=True)
    except Exception as e:
        logging.error(f"Error installing service: {e}")

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
        'thrusday' : 3,
        'friday' : 4,
        'saturday' : 5,
        'sunday' : 6,
    }
    # Convert each day word to num
    return [day_map[day] for day in days]

def get_available_processes():
    return {proc.info['name'].lower(): proc for proc in psutil.process_iter(['name']) if '.exe' in proc.info['name'].lower()}