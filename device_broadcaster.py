from typing import List
import struct
import socket
from threading import Timer
from zenlightsim.light_state_manager import LightStateManager

device_ident_opcode = 0

class DeviceBroadcaster(object):

    def __init__(self, uuid: str, strips: List[LightStateManager], socket: socket.socket):
        self.socket = socket
        self.init_socket()
        self.exit_flag = False

        self.broadcast_message = struct.pack(
            "!16sIII",
            uuid.encode("utf-8"),
            device_ident_opcode,
            0,
            len(strips)*3
        )

        for i in strips:
            self.broadcast_message += struct.pack("!BH", i.ident, i.length)

        #start the broadasting event loop        
        self.bcast_timer = Timer(5, self.broadcast)
        self.bcast_timer.start()


    def init_socket(self):
        if self.socket is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.socket.bind(("0.0.0.0", 0))

        
    def broadcast(self):
        if not self.exit_flag:
            # broadcast the message
            try:
                self.socket.sendto(self.broadcast_message, ("<broadcast>", 2000))
                # restart the timer
                self.bcast_timer = Timer(5, self.broadcast)
                self.bcast_timer.start()
            except Exception as err:
                print("Failed to broadcast device data", err)