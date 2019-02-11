import zmq

import tv.lg as tv 
from serialcontroller import open_serial_connection
from config import address

import os

def handle_set_input(data):
  pass

def handle_demonstrate(data):
  os.system("xdg-open /home/spoffy/Downloads/demonstrate.mp3")

def handle_power(data):
  device, state = data.split("&")
  print("Setting", device, "to", state)
  if device.lower() == "tv" or device.lower() == "television":
    if state.lower() == "on":
      with open_serial_connection() as ser:
        tv.TV(ser).set_power(True)
    elif state.lower() == "off":
      with open_serial_connection() as ser:
        tv.TV(ser).set_power(False)
    

handlers = dict()
handlers["SetInput"] = handle_set_input
handlers["Demonstrate"] = handle_demonstrate
handlers["SetPower"] = handle_power

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

