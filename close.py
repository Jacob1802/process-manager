from typing import List
import datetime as dt
import psutil
import json
import time
import sys
import os

appdata_dir = os.path.join(os.environ['APPDATA'], 'ProcessCloserService')

def set_process_termination(process):
    try:
        config_path = os.path.join(appdata_dir, 'config', 'config.json')
        config = load_config(config_path)

        process_data = config[process]
        start_time = dt.datetime.strptime(process_data['start_time'], "%H:%M").time()
        end_time = dt.datetime.strptime(process_data['end_time'], "%H:%M").time()
        days = convert_days_to_nums(process_data['days'])

        while True:
            now = dt.datetime.now()
            current_time = now.time()
            current_day = now.weekday()
            if current_day in days:
                if start_time <= current_time <= end_time:
                    terminate_process([process])
            
            time.sleep(10)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        return

def terminate_process(process_names: List[str]):
    """Function to close specified processes if they are running."""
    running_processes = {proc.info['name'].lower(): proc for proc in psutil.process_iter(['name']) if '.exe' in proc.info['name'].lower()}
    for name in process_names:
        process_name_lower = name.lower() + ".exe"
        if process_name_lower in running_processes.keys():
            running_processes[process_name_lower].terminate()

def load_config(config_file):
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return json.load(f)
    return {}

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

if __name__ == "__main__":
    set_process_termination(sys.argv[1])