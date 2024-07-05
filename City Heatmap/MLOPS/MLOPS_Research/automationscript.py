import subprocess
import signal
import time

# Find the process ID (PID) of the terminal
terminal_pid = subprocess.check_output(["pidof", "-s", "Terminal"]).decode().strip()

# Send the SIGINT signal (Ctrl+C) to the terminal
subprocess.run(["kill", "-INT", terminal_pid])

# Wait for a short time to allow the previous process to terminate
time.sleep(1)

# Run the streamlit command
subprocess.run(["streamlit", "run", "app.py"])
'''
import subprocess
import signal
import time

# Find the process ID (PID) of the Terminal
terminal_pid = subprocess.check_output(["pgrep", "-xq", "Terminal"]).decode().strip()

# Send the SIGINT signal (Ctrl+C) to the Terminal
subprocess.run(["kill", "-INT", terminal_pid])

# Wait for a short time to allow the previous process to terminate
time.sleep(1)

# Run the streamlit command
subprocess.run(["streamlit", "run", "app.py"])
'''