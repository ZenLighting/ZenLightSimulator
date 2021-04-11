import socket
import queue
import threading

class NetworkInputStream(threading.Thread):

    def __init__(self, input_socket, input_queue: queue.Queue):
        super().__init__()
        self.input_queue = input_queue
        self.exit_flag = False
        self.data_socket = input_socket
        self.init_socket()

    def init_socket(self):
        if self.data_socket is None:
            self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
            self.data_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.data_socket.bind(("" ,42000))

    def run(self):
        while not self.exit_flag:
            message, address = self.data_socket.recvfrom(1024)
            if message is not None:
                self.input_queue.put(message)
    
    # def init_socket()