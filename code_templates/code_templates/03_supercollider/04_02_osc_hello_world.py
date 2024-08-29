from pythonosc.udp_client import SimpleUDPClient

ip = "127.0.0.1"
port = 57120

msg = "Hello World."

client = SimpleUDPClient(ip, port)

client.send_message("/hello/world", msg)
