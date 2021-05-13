import struct
import pydantic
from typing import List

class ZenLightMessageData(pydantic.BaseModel):
    device_id: int # 1 byte
    opcode: int # 4 bytes
    flag_bytes: int # 4 bytes
    data_length: int # 2 bytes
    data: bytes # max value of short bytes

class ZenLightUpdateLightData(pydantic.BaseModel):
    index: int
    r_channel: int
    g_channel: int
    b_channel: int

class ZenLightMessageParser(object):

    @staticmethod
    def parse_raw_message(message_raw: bytes) -> ZenLightMessageData:
        header_len = struct.calcsize("!BIIH")
        (device_id, opcode, flags, data_len) = struct.unpack("!BIIH", message_raw[:header_len])
        data = message_raw[header_len:]
        return ZenLightMessageData(device_id=device_id, opcode=opcode, flag_bytes=flags, data_length=data_len, data=data)

    @staticmethod
    def parse_update_light_message(message: ZenLightMessageData) -> List[ZenLightUpdateLightData]:
        data = message.data
        data_len = message.data_length
        to_update_array = []
        
        for i in range(0, data_len, 4):
            index = data[i]
            r = data[i+1]
            g = data[i+2]
            b = data[i+3]
            to_update_array.append(ZenLightUpdateLightData(
                index=index,
                r_channel=r,
                g_channel=g,
                b_channel=b
            ))
        return to_update_array
