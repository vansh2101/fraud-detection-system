# Publishing to RabbitMQ 
import pika 
import json 
import base64

connection = pika.BlockingConnection(pika.ConnectionParameters(host="64.227.187.18", credentials=pika.PlainCredentials(username="anmol", password="12345")))
channel = connection.channel()
channel.queue_declare(queue="complaints")

# Creating payload
content = "" # concised text complaint  
original_text = "" #original complaint
# Handle the attached media file here
with open('example.mp3', 'rb') as file: 
    file_data = file.read()
    encoded_file = base64.b64encode(file_data).decode('utf-8')

message = {
    "text" : content,
    "original_text" : original_text,  
    "filename" : "example.mp3", 
    "file_type" : "audio/mp3", 
    "file_data" : encoded_file, 
    "metadata" : {}
}
message = json.dumps(message).encode('utf-8')

channel.basic_publish(exchange='', routing_key='complaints', body=message)