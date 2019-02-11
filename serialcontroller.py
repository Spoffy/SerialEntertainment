import serial

def open_serial_connection(settings, port = "/dev/ttyUSB0"):
  return serial.Serial(port
                     , baudrate=settings["baudrate"]
                     , bytesize=settings["bytesize"]
                     , parity=settings["parity"]
                     , stopbits=settings["stopbits"] 
                     , xonxoff=settings["flowcontrol"]
                     , timeout=10)

def transmit_bytes(data):
  with open_serial_connection() as ser:
    ser.write(data)
