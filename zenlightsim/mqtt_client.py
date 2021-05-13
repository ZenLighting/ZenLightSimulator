import string
import paho.mqtt.client as mqtt
import logging
from multiprocessing.queues import Queue
from multiprocessing import Process
import multiprocessing as mp

log = logging.getLogger(__name__)

class LightMQTTClient(object):

    def __init__(self, device_id: str, server_host: str, server_port: int=1883):
        self.client = mqtt.Client()
        self.device_id = device_id
        self.subscribed_channels = set()
        ctx = mp.get_context("spawn")
        self.input_message_queue = ctx.Queue()
        self.output_message_queue = ctx.Queue()

        self.client.on_connect = self.on_connect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message

        self.client.connect(server_host)

    @property
    def queue(self):
        return self.input_message_queue

    @property
    def output_queue(self):
        return self.output_message_queue

    def subscribe(self, client: mqtt.Client, channel):
        self.subscribed_channels.add(channel)
        for channel in self.subscribed_channels:
            client.subscribe(channel)
        log.info(f"Requested subscribe for {self.subscribed_channels}")
    
    def on_connect(self, client, userdata, flags, rc):
        # light devices listen for light messages on /device/<light_id>/input
        self.subscribe(client, f"device/{self.device_id}/input")

    def on_subscribe(self, client, userdata, mid, granted_qos):
        log.info("Subscribe sucessfull")
    
    def on_message(self, client, userdata, msg):
        log.info(f"Recieved message {msg.payload} on {msg.topic}")
        self.input_message_queue.put((msg.topic, msg.payload))
    
    def loop_proc(self):
        self.client.loop_forever()
