from typing import List
import datetime as dt
import utils
import time
import sys

def set_process_termination(process):
    try:
        # config_path = os.path.join(os.getcwd(), 'config.json')
        config = utils.load_config('C:\\Users\\user\\Documents\\Projects\\process-manager\\config.json')

        process_data = config[process]
        start_time = dt.datetime.strptime(process_data['start_time'], "%H:%M").time()
        end_time = dt.datetime.strptime(process_data['end_time'], "%H:%M").time()
        days = utils.convert_days_to_nums(process_data['days'])


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
    # Collect all running processes once
    running_processes = utils.get_availavle_processes()

    for name in process_names:
        process_name_lower = name.lower() + ".exe"

        if process_name_lower in running_processes.keys():
            running_processes[process_name_lower].terminate()


if __name__ == "__main__":
    set_process_termination(sys.argv[1])