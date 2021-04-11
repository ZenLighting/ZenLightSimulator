from light_state_manager import LightStateManager
from queue import Queue, Empty
from message_parser import ZenLightMessageParser, ZenLightUpdateLightData
from typing import List
from light_state_manager import LightStateManager
from threading import Thread

class LightInputStreamConnector(Thread):

    def __init__(self, light_state_managers: List[LightStateManager], input_queue: Queue):
        super().__init__()
        self.input_queue = input_queue
        self.light_state_managers = light_state_managers
        self.light_state_manager_id_map = {}
        self.exit_flag = False

        for light_manager in self.light_state_managers:
            self.light_state_manager_id_map[light_manager.ident] = light_manager
    
    def run(self):
        self.consumer_input()

    def consumer_input(self):
        while not self.exit_flag:
            try:
                message = self.input_queue.get(1)
                # parse message
                message_data = ZenLightMessageParser.parse_raw_message(message)
                if message_data.opcode == 0:
                    # was an update message
                    updates_list = ZenLightMessageParser.parse_update_light_message(message_data)
                    # update the device specified
                    self.update_light_state(message_data.device_id, updates_list)
            except Empty:
                continue

    def update_light_state(self, state_manager_id: int, updates_list: List[ZenLightUpdateLightData]):
        state_manager: LightStateManager = self.light_state_manager_id_map[state_manager_id]
        for light_update in updates_list:
            state_manager.update_light(light_update.index, light_update.r_channel, light_update.g_channel, light_update.b_channel)
        state_manager.display()    
        