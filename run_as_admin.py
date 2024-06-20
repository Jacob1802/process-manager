import subprocess
import ctypes
import sys

def run_as_admin(cmd, wait=True):
    """Run a command as an administrator."""
    try:
        params = ' '.join([f'"{c}"' for c in cmd])
        shell32 = ctypes.windll.shell32
        ret = shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 0)
        if wait:
            subprocess.Popen(cmd, shell=True).wait()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_as_admin(sys.argv[1:])
    else:
        print("Usage: run_as_admin.py <script_to_run> [arguments]")