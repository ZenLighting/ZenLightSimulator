import socket
import struct
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("localhost")

#send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

data_bytes = struct.pack("!BBBB", 0, 0, 255, 255)

header = struct.pack("!BIIH", 0, 0, 0, len(data_bytes))
message = header + data_bytes

client.publish("device/Sim1/input", message)
#send_sock.sendto(message, ("localhost", 42000))