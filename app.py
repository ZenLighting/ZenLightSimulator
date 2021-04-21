from device_broadcaster import DeviceBroadcaster
from light_state_manager import LightStateManager
from network_input_stream import NetworkInputStream
from light_input_connector import LightInputStreamConnector
import uuid
import queue

# initialize any objects
strip1 = LightStateManager(20)
broadcaster = DeviceBroadcaster(str(uuid.uuid4()), [strip1], None)

input_queue = queue.Queue()
network_input_stream = NetworkInputStream(None, input_queue)
connector = LightInputStreamConnector([strip1], input_queue)
# start any threaded operations
#broadcaster.start()
connector.start()
network_input_stream.start()