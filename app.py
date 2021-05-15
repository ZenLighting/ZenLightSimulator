from device_broadcaster import DeviceBroadcaster
from zenlightsim.light_state_manager import LightStateManager
from network_input_stream import NetworkInputStream
from zenlightsim.light_input_connector import LightInputStreamConnector
import uuid
import queue
from zenlightsim.mqtt_client import LightMQTTClient
from multiprocessing import Process
import multiprocessing as mp
from threading import Thread
import logging
import paho.mqtt.client as mqtt
import time
from threading import Timer
import json
from zenlightsim.mqtt_info_channel import MQTTRegistry
#def send_delayed_message(client: mqtt.Client):
    #print("Produced")
    #client.publish("device/Sim1/input", json.dumps({"Hello": "hello"}).encode('utf-8'))

logging.basicConfig(level=logging.DEBUG)
mp.set_start_method('spawn')
# initialize any objects
mqtt_client = LightMQTTClient("Sim1", "localhost")

strip1 = LightStateManager(20, "Sim1")
strip1_manager = LightInputStreamConnector([strip1], mqtt_client.queue)
mqtt_registry = MQTTRegistry(strip1, mqtt_client.client)

Thread(target=mqtt_client.client.loop_forever).start()
strip1_manager.start()
mqtt_registry.start()



"""broadcaster = DeviceBroadcaster(str(uuid.uuid4()), [strip1], None)

input_queue = queue.Queue()
network_input_stream = NetworkInputStream(None, input_queue)
connector = LightInputStreamConnector([strip1], input_queue)
# start any threaded operations
#broadcaster.start()
connector.start()
network_input_stream.start()"""
