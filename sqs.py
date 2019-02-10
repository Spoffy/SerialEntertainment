import credentials
import boto3
from zeromqclient import SerialClient

# Amazon Setup
#==============
MessageGroup = "SerialCommands"

session = boto3.Session(
  aws_access_key_id = credentials.AWS_ACCESS_KEY_ID,
  aws_secret_access_key = credentials.AWS_SECRET_ACCESS_KEY,
  region_name = "eu-west-1"
)

sqs = session.resource("sqs")

queue = sqs.get_queue_by_name(QueueName="SerialEntertainment.fifo")

# ZeroMQ Setup
#==============
client = SerialClient()

while True:
  for message in queue.receive_messages():
    #Translate here
    print(message.body)
    message.delete()

    client.send_message(message.body)
