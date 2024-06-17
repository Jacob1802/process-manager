import subprocess
import logging
import psutil
import json
import os

def is_gamecloser_running(service_name):
    """Check if the GameCloser service is running."""
    try:
        result = subprocess.run(['sc', 'query'], capture_output=True, text=True, check=True)
        lines = result.stdout.split('\n')
        for line in lines:
            if service_name in line:
                return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred: {e}")
    return False


def create_service(service_name, executable):
    # WORKING_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game_closer.py")
    dest_folder = get_dest_folder()
    # log_path = os.path.join(dest_folder, 'Logs', 'output.log')

    nssm_path = os.path.join(dest_folder, 'nssm-2.24\\win64\\nssm.exe')
    if not nssm_path:
        print("Error: Path to NSSM not provided.")
        return
    
    # exe_path = os.path.join(dest_folder, 'game_closer.exe')
    exe_path = os.path.join(dest_folder, 'C:\\Users\\user\\Documents\\Projects\\process-manager\\close.py')

    try:
        subprocess.run([nssm_path, 'install', service_name, executable, exe_path, service_name])
        subprocess.run([nssm_path, 'set', service_name, 'AppStdout', 'C:\\Users\\user\\Documents\\Projects\\process-manager\\output.log'], check=True)
        subprocess.run([nssm_path, 'set', service_name, 'AppStderr', 'C:\\Users\\user\\Documents\\Projects\\process-manager\\output.log'], check=True)
        # Set the working directory
        # subprocess.run([nssm_path, "set", service_name, "AppDirectory", WORKING_DIRECTORY], check=True)

        subprocess.run([nssm_path, 'start', service_name], check=True)
        print(f"Service '{service_name}' started successfully.")

    except Exception as e:
        print(f"Error installing service: {e}")


def get_dest_folder():
    parent = os.path.dirname(os.getcwd())
    return os.path.join(parent, 'Downloads', 'game-manager')


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