from threading import Thread
import subprocess

# Path to your Node.js script
node_script = 'server.js'

def start_node(node_script):
    # Start the Node.js script in the background
    process = subprocess.Popen(['node', node_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Read output in real-time
    try:
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output)
    except KeyboardInterrupt:
         print("Terminating the process...")
         process.terminate()

    # Capture any remaining output after the loop
    stdout, stderr = process.communicate()
    if stdout:
        print('Final Output:', stdout.strip())
    if stderr:
        print('Error:', stderr.strip())

# Make a main function to allow the script to be run in a separate thread.
def main(node_script):
    node_Thread = Thread(target=start_node, args=(node_script,))
    node_Thread.start()

main(node_script)
