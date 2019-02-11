import serial

class SerialDevice:
  serial_config = {
    "baudrate": 9600,
    "bytesize": serial.EIGHTBITS,
    "parity": serial.PARITY_NONE,
    "stopbits": serial.STOPBITS_ONE,
    "flowcontrol": False
  }

  def __init__(self, port):
    self.port = port
