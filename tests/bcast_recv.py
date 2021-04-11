import socket

sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sockfd.bind(("", 2000))

print("Socket initialized listening for messages")

while True:
    message, addy = sockfd.recvfrom(1024)
    print(f"Got message: {message} from {addy}")