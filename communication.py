import numpy as np
from capsule import *
import struct
import serial

ser = None

def teensyInit():
    global ser
    # Arduino connected on USB serial, use try, except to try to connect
    try:
        ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0)
        print("Teensy connected")
    except:
        print("Teensy not connected")

# Example of using the Capsule class
class Foo:
    pass

class LightPoint:
    def __init__(self, name, isVisible, x, y, age):
        self.name = str(name)
        self.isVisible = bool(isVisible)  # Ensure boolean type
        self.x = int(x)  # Ensure integer type
        self.y = int(y)  # Ensure integer type
        self.age = int(age)

def handle_packet(packetId, dataIn, lenIn):
    print(f"Received packet with ID {packetId}")

capsule_instance = Capsule(lambda packetId, dataIn, len: handle_packet(packetId, dataIn[:len], len))

# Send target to arduino via USB serial
def sendTargetToTeensy(pointToSendIn, cameraID, Kp, maxSpeed):
    global sock
    # Send the target point to the teensy, the structure should be copied in a byte array then encoded then sent
    packet_id = 0x01
    # Pack the struct in a byte array

    pointToSend = LightPoint(pointToSendIn.name, pointToSendIn.isVisible, pointToSendIn.x, pointToSendIn.y, pointToSendIn.age)

    pointToSendName = str(pointToSend.name)
    payload_data = struct.pack('4siiiiiff', pointToSendName.encode('utf-8'), pointToSend.isVisible, pointToSend.x, pointToSend.y, pointToSend.age, cameraID, Kp, maxSpeed)
    packet_length = len(payload_data)
    encoded_packet = capsule_instance.encode(packet_id, payload_data, packet_length)
    # Print the encoded packet
    #print(f"Encoded Packet: {encoded_packet}")
    # Convert encoded_packet to a bytearray
    encoded_packet = bytearray(encoded_packet)

    try:
        # Send the encoded packet
        ser.write(encoded_packet)
        print("Data sent")
    except Exception as e:
        print(f"Error occurred while sending data: {e}")
