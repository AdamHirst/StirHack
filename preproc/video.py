import cv2

class FaceDetector:

	def __init__(self):
		self.__face_cascade = cv2.CascadeClassifier()
		self.__face_profile_cascade = cv2.CascadeClassifier()
		self.__body_cascade = cv2.CascadeClassifier()
		self.mainCapture = cv2.VideoCapture(-1)
		self.resetCaptureDevice()

	# useful for debugging
	def __showImage(self, img):
		cv2.imshow('img', img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	def openCapture(self):
		if not self.mainCapture.isOpened():
			self.mainCapture.open(-1)
			self.__face_cascade.load('haar_profiles/haarcascade_frontalface_default.xml')
			self.__face_profile_cascade.load('haar_profiles/haarcascade_profileface.xml')
			self.__body_cascade.load('haar_profiles/haarcascade_fullbody.xml')

	def closeCapture(self):
		if self.mainCapture.isOpened():
			self.mainCapture.release()

	def resetCaptureDevice(self):
		self.closeCapture()
		self.openCapture()

	# returns true, along with the image in question, and a list of x,y,w,h
	# tuples, if the main camera detects a face - if the main camera fails to
	# grab a frame or does not detect a face then false is returned
	def hasFace(self):
		read, frame = self.mainCapture.read()
		if not read:
			return False, [[[]]], ()
		# find out if the frame contains any faces
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = self.__face_cascade.detectMultiScale(gray, 1.1, 2)
		if len(faces) > 0:
			return True, frame, faces
		else:
			return False, [[[]]], ()
