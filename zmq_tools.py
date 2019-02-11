import zmq
from config import address

# Connect to ZeroMQ instance
class ZeroMQClient:
  def __init__(self):
    self.context = zmq.Context()
    self.socket = self.context.socket(zmq.REQ)
    self.socket.connect(address)

  def send_message(self, message):
    self.socket.send_string(message)
    response = self.socket.recv_string()
    if response != None:
      return True
    return False

class ZeroMQServer:
  def __init__(self):
    self.context = zmq.Context()
    self.socket = self.context.socket(zmq.REP)
    self.socket.bind(address)
