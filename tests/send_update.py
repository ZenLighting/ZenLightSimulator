import socket
import struct

send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)


data_bytes = struct.pack("!BBBB", 0, 0, 255, 255)

header = struct.pack("!BIIH", 0, 0, 0, len(data_bytes))
message = header + data_bytes

send_sock.sendto(message, ("localhost", 42000))