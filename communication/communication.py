# communication/communication.py

import os
import paramiko
from pythonosc.udp_client import SimpleUDPClient

# OSC Client Configuration
osc_ip = "127.0.0.1"  # IP of the OSC server (running on the destination Pi)
osc_port = 57120       # Port of the OSC server

# Directories
LOCAL_OUTPUT_DIR = '/home/lab03/Desktop/intertotem/it-u-intertotem/output'  # Directory where the WAV files are generated on the source Pi
REMOTE_INPUT_DIR = '/home/totem/Desktop/intertotem/it-u-intertotem/input'   # Directory on the destination Pi where files should be copied

# Destination Pi's SSH details
destination_ip = '192.168.1.129'  # IP address of the destination Raspberry Pi
username = 'totem'                   # SSH username (typically 'pi')
password = 'totem'         # SSH password (or set up SSH keys for passwordless login)

# Initialize OSC client
client = SimpleUDPClient(osc_ip, osc_port)

def copy_file_to_pi(local_path, remote_path):
    """
    Copies a WAV file from the local directory to the remote Raspberry Pi and sends an OSC message upon completion.

    Parameters:
        local_path (str): The path to the local file to be copied.
        remote_path (str): The path on the remote Pi where the file will be copied.
    """
    try:
        # Set up SSH and SFTP clients
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(destination_ip, username=username, password=password)
        sftp = ssh.open_sftp()
        
        # Copy the file to the remote input directory
        sftp.put(local_path, remote_path)
        print(f"File copied to {remote_path}")
        
        # Close SFTP session
        sftp.close()
        ssh.close()

        # Send OSC message to notify that the file has been copied
        client.send_message("/file/copied", remote_path)
        print(f"OSC notification sent for {remote_path}")

    except Exception as e:
        print(f"Error copying file {local_path}: {e}")

def main():
    """
    Monitors the local output directory for new WAV files and copies them to the remote Pi.
    """
    # Monitor the LOCAL_OUTPUT_DIR for new files
    print("Monitoring output directory for new files...")
    for filename in os.listdir(LOCAL_OUTPUT_DIR):
        # Check for WAV files only
        if filename.endswith(".wav"):
            local_path = os.path.join(LOCAL_OUTPUT_DIR, filename)
            remote_path = os.path.join(REMOTE_INPUT_DIR, filename)
            copy_file_to_pi(local_path, remote_path)

if __name__ == "__main__":
    main()
