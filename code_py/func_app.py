from flask import jsonify
import signal
import subprocess
import os
import time
from code_py.config import pid_file, core

last_heartbeat = time.time()
process = None 

def check_heartbeat():
    global last_heartbeat
    while True:
        time.sleep(10) 
        if time.time() - last_heartbeat > 10:
            print("No heartbeat received. Shutting down server.")
            terminate_process()  
            os.kill(os.getpid(), signal.SIGINT) 

def start_executable():
    global process
    if os.path.isfile(pid_file):
        print("Process is already running.")
        return

    executable_path = core
    if os.path.isfile(executable_path):
        process = subprocess.Popen([executable_path], shell=True)
        with open(pid_file, 'w') as f:
            f.write(str(process.pid))
    else:
        print(f"Error: {executable_path} not found.")

def terminate_process():
    global process
    if process is not None:
        process.terminate()
        process.wait()
        os.remove(pid_file)  


#post#post#post#post#post#post#post#post#post#post#post#post#post#post#post#post#post#post#post#post
#post#post#post#post#post#post#post#post#post#post#post#post#post#post#post#post#post#post#post#post
#post#post#post#post#post#post#post#post#post#post#post#post#post#post#post#post#post#post#post#post

def heartbeat():
    global last_heartbeat
    last_heartbeat = time.time()
    return jsonify({'status': 'ok'}), 200


