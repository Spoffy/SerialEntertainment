import serial

setid = 0x00

INPUT_HDMI = 0b01110000

def command(command_1, command_2, setid, data):
  #Format is an ascii string converted to bytes of structure
  # "xx 00 00\r"
  command_bytes = bytearray(command_1 + command_2 + " " + hex(setid)[2:] + " " + hex(data)[2:] + "\r", encoding="ascii")
  return command_bytes

create_set_power_command = lambda data: command("k", "a", setid, data)
create_set_muted_command = lambda data: command("k", "e", setid, data)
create_set_volume_command = lambda data: command("k", "f", setid, data)
create_set_input_command = lambda data: command("x", "b", setid, data)

#============================================
#================= PUBLIC ===================
#============================================

serial_config = {
  "baudrate": 9600,
  "bytesize": serial.EIGHTBITS,
  "parity": serial.PARITY_NONE,
  "stopbits": serial.STOPBITS_ONE,
  "flowcontrol": False
}

class TV():
  def __init__(self, serial_port):
    super().__init__(serial_port)

  def set_power(self, state):
    data = 0x01 if state == True else 0x00
    self.transmit(create_set_power_command(data))

  def set_muted(self, state):
    data = state == 0x00 if state == True else 0x01
    self.transmit(create_set_muted_command(data))
  
  def set_volume(self, percentage):
    data = max(0, min(percentage, 100))
    self.transmit(create_set_volume_command(data))

  def set_input(self, input_type, number):
    if input_type == "hdmi":
      input_number = number - 1
      if input_number < 0 or input_number > 2:
        print("Unsupported HDMI input: " + str(number))
        return
      data = INPUT_HDMI | input_number
      self.transmit(create_set_input_command(data))
    else:
      print("Unsupported input type: " + input_type)
