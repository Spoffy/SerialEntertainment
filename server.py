import zmq
from config import address

import os

def handle_duck(data):
  print("Ducks do a", data)

def handle_set_input(data):
  print("Setting input to " + data)

def handle_demonstrate(data):
  os.system("xdg-open /home/spoffy/Downloads/demonstrate.mp3")

handlers = dict()
handlers["Ducks"] = handle_duck
handlers["SetInput"] = handle_set_input
handlers["Demonstrate"] = handle_demonstrate

def parse_command(message):
  pair = message.split(":")
  #Assumes valid command, add error handling
  return {
    "command": pair[0],
    "data": len(pair) > 1 and pair[1] or ""
  }

def dispatch_command(command):
  print(command)
  try:
    handlers[command["command"]](command["data"])
  except KeyError:
    print("No valid handler")

# Set up ZeroMQ
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(address)

while True:
  message = socket.recv_string()
  socket.send_string("Command received")

  command = parse_command(message)
  dispatch_command(command)

