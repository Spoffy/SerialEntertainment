import serial
import commands
from enum import Enum

DellLabMonitor = {
  "baudrate": 9600,
  "bytesize": serial.EIGHTBITS,
  "parity": serial.PARITY_NONE,
  "stopbits": serial.STOPBITS_ONE,
  "flowcontrol": False
}

def open_serial_connection(port = "/dev/ttyUSB0", settings = DellLabMonitor):
  return serial.Serial("/dev/ttyUSB0"
                     , baudrate=settings["baudrate"]
                     , bytesize=settings["bytesize"]
                     , parity=settings["parity"]
                     , stopbits=settings["stopbits"] 
                     , xonxoff=settings["flowcontrol"]
                     , timeout=10)

with open_serial_connection() as ser:
  print(ser.name)
  print(ser.is_open)
  print("Writing")
  print(commands.GetMonitorNameCommand().to_bytes())
  #ser.write(commands.GetMonitorNameCommand().to_bytes())
  ser.write(bytes([0x37, 0x51, 0x03, 0xEA, 0x20, 0x01, 0xAE]))
  #ser.write(bytes.fromhex('375102eb20af'))
  print("Reading")
  print(ser.read(5).hex())

