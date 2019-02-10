READ_CONST = 0xEB
WRITE_CONST = 0xEA

class Command:
  def __init__(self):
    self.head_0 = 0x37
    self.head_1 = 0x51
    self.length = 0
    self.readwrite = READ_CONST
    self.cmd = 0
    self.data = []
    self.fixed_checksum = None

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

class GetMonitorNameCommand(Command):
  def __init__(self):
    super().__init__()
    self.length = 0x02
    self.readwrite = READ_CONST
    self.cmd = 0x01
    self.fixed_checksum = 0x8E
