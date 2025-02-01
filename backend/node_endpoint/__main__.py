import os
import subprocess
from threading import Thread

# Define the relative path to the server.js file from server.py
node_script = os.path.join(os.path.dirname(__file__), 'backend', 'server.js')

def start_node(node_script):
    # Ensure the full path is correct and the directory exists
    cwd = os.path.dirname(node_script)  # This should be the 'backend' folder
    process = subprocess.Popen(
        ['node', node_script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=cwd  # Ensure the Node process runs in the backend directory
    )

    try:
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
    except KeyboardInterrupt:
        print("Terminating the process...")
        process.terminate()

    stdout, stderr = process.communicate()
    if stdout:
        print('Final Output:', stdout.strip())
    if stderr:
        print('Error:', stderr.strip())

def main():
    node_thread = Thread(target=start_node, args=(node_script,))
    node_thread.start()

if __name__ == "__main__":
    main()
