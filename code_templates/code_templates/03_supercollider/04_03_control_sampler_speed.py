import sys

from pythonosc.udp_client import SimpleUDPClient

ip = "127.0.0.1"
port = 57120

speed = float(sys.argv[1])

client = SimpleUDPClient(ip, port)

client.send_message("/control/sampler/speed", speed)
