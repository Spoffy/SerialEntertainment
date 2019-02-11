import serial
import tv.lg as tv
from enum import Enum

def open_serial_connection(port = "/dev/ttyUSB0", settings = tv.serial_config):
  return serial.Serial("/dev/ttyUSB0"
                     , baudrate=settings["baudrate"]
                     , bytesize=settings["bytesize"]
                     , parity=settings["parity"]
                     , stopbits=settings["stopbits"] 
                     , xonxoff=settings["flowcontrol"]
                     , timeout=10)

def transmit_bytes(data):
  with open_serial_connection() as ser:
    ser.write(data)

def debug():
  with open_serial_connection() as ser:
    data = tv.set_volume(40)
    print(data.hex())
    ser.write(tv.set_volume(90))
    #ser.write(tv.power_on)
    print(ser.read(7))
