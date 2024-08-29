import sys

from pythonosc.udp_client import SimpleUDPClient

ip = "127.0.0.1"
port = 57120

src_buffer = int(sys.argv[1])

client = SimpleUDPClient(ip, port)

client.send_message("/control/sampler/src", src_buffer)
