import os
import sys

import devices.tv.lg
import zmq_tools
from exceptions import *
from serialcontroller import open_serial_connection
from config import address

#########################
#### Device Handling ####
#########################

devices = {
  "tv": devices.tv.lg.MyLGTV,
  "television": devices.tv.lg.MyLGTV
}

def find_device(device_name):
  try:
    return devices[device_name.lower()]
  except KeyError:
    raise DeviceNotFoundError

def get_device_then(command_handler_to_call):
  def result(device_name, *args):
    device = find_device(device_name)
    with open_serial_connection(device.serial_config) as ser:
      device_instance = device(ser)
      return command_handler_to_call(device_instance, *args)

  return result

##################
#### Commands ####
##################

def handle_demonstrate():
  os.system("xdg-open /home/spoffy/Downloads/demonstrate.mp3")

def set_power(device_instance, state):
  print("Setting power")
  if state.lower() == "on":
    device_instance.set_power(True)
  elif state.lower() == "off":
    device_instance.set_power(False)

def set_muted(device_instance, state):
  if state.lower() == "on":
    device_instance.set_muted(True)
  elif state.lower() == "off":
    device_instance.set_muted(False)

def set_volume(device_instance, volume):
  device_instance.set_volume(volume)


def set_input(device_instance, input_type, input_number):
  device_instance.set_input(input_type, input_number)

handlers = dict()
handlers["demonstrate"] = handle_demonstrate
handlers["setpower"] = get_device_then(set_power)
handlers["setmuted"] = get_device_then(set_muted)
handlers["setvolume"] = get_device_then(set_volume)
handlers["setinput"] = get_device_then(set_input)

########################
####### COMMANDS #######
########################

""" 
Commands have structure: Command:param1:param2:...params
"""

def parse_command(message):
  message = message.lower()
  segments = message.split(":")
  command = segments[0]
  parameters = segments[1:] if len(segments) > 1 else []
  #Assumes valid command, add error handling
  return {
    "command": command,
    "parameters": parameters
  }

def dispatch_command(command):
  try:
    print("Running", command)
    handlers[command["command"]](*command["parameters"])
  except KeyError:
    print("No valid handler")
  except DeviceNotFoundError:
    print("A device with that name could not be found")
  except OperationNotSupportedError:
    print("That device does not support that operation")

##########################
########## MAIN ##########
##########################

# Set up ZeroMQ
server = zmq_tools.ZeroMQServer()

print("Starting server listening on " + address)

while True:
  try:
    message = server.socket.recv_string()
    server.socket.send_string("Command received")

    command = parse_command(message)
    dispatch_command(command)
  except FileNotFoundError:
    print("File not found error - is the serial cable is connected?", file=sys.stderr)
  except Exception as e:
    print("An exception occurred:\n", e, file=sys.stderr)

