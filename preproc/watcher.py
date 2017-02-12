import video
import time
import threading
import cv2
import os

running = False

# Blocks until a face is detected by the default camera
def waitForFace(detector):
	# busy wait for a result
	face, img, _, t = detector.hasFace()
	while not face:
		face, img, _, t = detector.hasFace()
	return img, t

def writeImage(img, timestamp):
	name = "images/" + str(timestamp) + ".png"
	print "attempting to write image " + name
	if os.path.isdir("./images"):
		if os.path.isfile(name):
			os.remove(name)
		cv2.imwrite(name, img)
	else:
		raise ValueError("./images is not a directory!")

def uploadImage(timestamp):
	print "uploading image " + str(timestamp)
	os.remove("./images/" + str(timestamp) + ".png")

def watch():
	running = True
	detector = video.FaceDetector()
	while running:
		img, timestamp = waitForFace(detector)
		print "found potential face"
		th = threading.Thread(target=uploadImage, args=(timestamp, ))
		writeImage(img, timestamp)
		th.start()
		time.sleep(1)

watch()
