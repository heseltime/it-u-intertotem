import os
import paramiko
from pythonosc.udp_client import SimpleUDPClient

# List of destination IPs for multiple Raspberry Pis
destination_ips = ["192.168.1.129"]  # Add more IP addresses as needed
osc_port = 57120  # Port of the OSC server

# Directories
LOCAL_OUTPUT_DIR_BASE = '/home/lab03/Desktop/intertotem/it-u-intertotem/'  # Directory where the WAV files are generated on the source Pi
REMOTE_INPUT_DIR = '/home/totem/Desktop/intertotem/it-u-intertotem/input'  # Directory on the destination Pi where files should be copied

# SSH credentials
username = 'totem'  # SSH username
password = 'totem'  # SSH password

def copy_file_to_pi(local_path, remote_path, destination_ip=destination_ips):
    """
    Copies a WAV file from the local directory to a remote Raspberry Pi and sends an OSC message upon completion.

    Parameters:
        local_path (str): The path to the local file to be copied.
        remote_path (str): The path on the remote Pi where the file will be copied.
        destination_ip (str): The IP address of the destination Raspberry Pi.
    """
    try:
        # Set up SSH and SFTP clients
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(destination_ip, username=username, password=password)
        sftp = ssh.open_sftp()
        print(f"Connecting via SSH to {destination_ip}")
        
        # Copy the file to the remote input directory
        print(f"Attempting to copy {LOCAL_OUTPUT_DIR_BASE + local_path} to {remote_path} on {destination_ip}")
        sftp.put(LOCAL_OUTPUT_DIR_BASE + local_path, remote_path)
        print(f"File copied to {destination_ip}:{remote_path}")
        
        # Close SFTP session
        sftp.close()
        ssh.close()

        # Initialize OSC client and send OSC message to notify that the file has been copied
        client = SimpleUDPClient(destination_ip, osc_port)
        client.send_message("/file/copied", remote_path)
        print(f"OSC notification sent to {destination_ip} for {remote_path}")

    except Exception as e:
        print(f"Error copying file to {destination_ip}: {e}")

def main():
    """
    Monitors the local output directory for new WAV files and copies them to each remote Pi in the list.
    """
    print("Monitoring output directory for new files...")
    for filename in os.listdir(LOCAL_OUTPUT_DIR_BASE):
        # Check for WAV files only
        if filename.endswith(".wav"):
            local_path = os.path.join(LOCAL_OUTPUT_DIR_BASE, filename)
            remote_path = os.path.join(REMOTE_INPUT_DIR, filename)
            # Iterate over each IP address and copy the file
            for ip in destination_ips:
                copy_file_to_pi(local_path, remote_path, ip)

if __name__ == "__main__":
    main()
