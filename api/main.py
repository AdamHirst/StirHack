#from bottle import route, run, template
import pika
import sqlite3
import aws
import json
import datetime
from time import gmtime, strftime

#@route('/hello/<name>')
#def index(name):
#    return template('<b>Hello {{name}}</b>!', name=name)

#run(host='localhost', port=8080)

#aws.new_store(1)
print "Loading imagees"
dt= strftime("%Y-%m-%d %H:%M:%S", gmtime())

item = aws.FaceItem(1, 1, dt,open("a1.jpg", "rb").read())
item1 = aws.FaceItem(1, 1, dt, open("a2.jpg", "rb").read())
item2 = aws.FaceItem(1, 1, dt, open("m2.jpg", "rb").read())
print "Done. Sending to queue"
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='face')
channel.basic_publish(exchange='',routing_key='face',body=aws.serializeFaceItem(item))
channel.basic_publish(exchange='',routing_key='face',body=aws.serializeFaceItem(item1))
channel.basic_publish(exchange='',routing_key='face',body=aws.serializeFaceItem(item2))

print("Done sending, rabbitmq now listening for messages'")

aws.start_rabbitmq_listen()