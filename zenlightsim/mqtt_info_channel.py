from queue import Queue
from threading import Thread
import time
from zenlightsim.light_state_manager import LightStateManager
import json
from paho.mqtt.client import Client

class MQTTRegistry(Thread):

    def __init__(self, light_state: LightStateManager, mqtt_client: Client):
        Thread.__init__(self)
        self.dId = light_state._identifier
        self.state = light_state
        self.output = mqtt_client

    def run(self):
        while True:
            # create mqtt message
            message = {
                "dId": self.dId,
                "type": "light",
                "data": {
                    "state": self.state._light_array
                }
            }
            # topic, data
            self.output.publish("device/registry", payload=json.dumps(message).encode('utf-8'))
            # only send message once a second
            time.sleep(1)
