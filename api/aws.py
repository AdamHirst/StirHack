import boto3
import pika
import json
import base64
import db

MAX_FACES = 20
THRESHOLD_PERCENT = 60

class FaceItem:

	def __init__(self, store_id, camera_id, timestamp, image_data):
		self.store_id = store_id
		self.camera_id = camera_id
		self.timestamp = timestamp
		self.image_data = image_data

def serializeFaceItem( face):
	image = base64.b64encode(face.image_data)
	return json.dumps({"timestamp" : face.timestamp, "store_id" : face.store_id, "camera_id" : face.camera_id, "image_data": image})


def deserializeFaceItem( jsonStr):
	j = json.loads(jsonStr)
	image = base64.b64decode(j["image_data"])
	return FaceItem(j['store_id'], j['camera_id'], j['timestamp'], image)

class AwsFaceClient:

	def __init__(self):
		self._client = boto3.client('rekognition')

	def create_new_collection(self, collection_name):
		return self._client.create_collection(CollectionId=collection_name)

	def add_face(self, collection_name, image_bytes):
		return self._client.index_faces(
		    CollectionId=collection_name,
		    Image={
		        'Bytes': image_bytes
		    },
		    DetectionAttributes=[
		        'DEFAULT'
		    ])

	def search_faces(self, collection_name, aws_face_id):
		print "Searching in {} for {}".format(collection_name, aws_face_id)
		return self._client.search_faces(
		   CollectionId=collection_name,
		   FaceId=aws_face_id,
		   MaxFaces=MAX_FACES)

	def list_faces(self, collection_name):
		paginator =  self._client.get_paginator('list_faces')
		return paginator.paginate(
		    CollectionId=collection_name,
		    PaginationConfig={
		        'MaxItems': 123,
		        'PageSize': 123
		    }
		)

	def search_face_by_image(self, collection_name, image_data):
		return self._client.search_faces_by_image(
	    CollectionId=collection_name,
	    Image={
	        'Bytes': image_data
	    })

awsClient =  AwsFaceClient()
database = db.Db()
for k, v in  database.occurence_frequency('2017-02-11 23:39:00', '2017-05-11 23:42:00').iteritems():
	print "{}: {}".format(k, v)

class AwsFaceCollection:

	def __init__(self, client, collection_name):
		self.collection = collection_name
		self.client = client

	def add_face(self, image_bytes):
		return self.client.add_face(self.collection, image_bytes)

	def search_faces(self, aws_face_id):
		return self.client.search_faces(self.collection, aws_face_id)

	def list_faces(self):
		return self.client.list_faces(self.collection)

	def search_face_by_image(self, image_data):
		return self.client.search_face_by_image(self.collection, image_data)


def on_faceitem_recieved(ch, method, properties, body):
	face = deserializeFaceItem(body)
	collection = AwsFaceCollection(awsClient, str(face.store_id))

	searchAttempt = collection.search_face_by_image(face.image_data)
	faceMatches = searchAttempt["FaceMatches"]
	if len(faceMatches) == 0:
		# Failed to find, add to db
		print("No face found, adding to db")
		addedFace = collection.add_face(face.image_data)
		faceRecords = addedFace["FaceRecords"]
		if len(faceRecords) == 0:
			return 
		faceRecord = faceRecords[0]
		fid = faceRecord["Face"]["FaceId"]

		# Add to Person database
		database.add_new_unique_person(fid)
		return
	else:
		print("Found faces - addding occurance to database")
		bestMatch = faceMatches[0]
		fid = bestMatch["Face"]["FaceId"]
		personId = database.person_id_from_face_id(fid)
		if personId is not None:
			database.add_person_occurance(face.store_id, face.camera_id, face.timestamp, personId)

def start_rabbitmq_listen():
	# TODO change from localhost
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()

	channel.queue_declare(queue='face')
	channel.basic_consume(on_faceitem_recieved, queue='face', no_ack=True)
	channel.start_consuming()

def new_store(store_id):
	return awsClient.create_new_collection(str(store_id))