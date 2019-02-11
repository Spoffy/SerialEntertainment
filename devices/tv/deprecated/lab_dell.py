READ_CONST = 0xEB
WRITE_CONST = 0xEA

serial_config = {
  "baudrate": 9600,
  "bytesize": serial.EIGHTBITS,
  "parity": serial.PARITY_NONE,
  "stopbits": serial.STOPBITS_ONE,
  "flowcontrol": False
}

class Command:
  def __init__(self):
    self.head_0 = 0x37
    self.head_1 = 0x51
    self.length = 0
    self.readwrite = READ_CONST
    self.cmd = 0
    self.data = []
    self.fixed_checksum = None
    self.response_length = 0

  @property
  def checksum(self):
    if self.fixed_checksum:
      return self.fixed_checksum
    return None

  def to_bytes(self):
    data_as_integers = [self.head_0, self.head_1, self.length, self.readwrite, self.cmd]
    for data_item in self.data:
      data_as_integers.append(data_item)
    data_as_integers.append(self.checksum)
    return bytearray(data_as_integers)

class MonitorNameCommand(Command):
  def __init__(self):
    super().__init__()
    self.length = 0x02
    self.readwrite = READ_CONST
    self.cmd = 0x01
    self.fixed_checksum = 0x8E
    self.response_length = 0

class PowerCommand(Command):
  def __init__(self):
    super().__init__()
    self.length = 0x03
    self.readwrite = WRITE_CONST
    self.cmd = 0x20
    self.response_length = 8

class TurnOnCommand(PowerCommand):
  def __init__(self):
    super().__init__()
    self.data.append(0x01)
    self.fixed_checksum = 0xAE

class TurnOffCommand(PowerCommand):
  def __init__(self):
    super().__init__()
    self.data.append(0x00)
    self.fixed_checksum = 0xAF

:wq

