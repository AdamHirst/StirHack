import video
import cv2

fd = video.FaceDetector()
fd.openCapture()
ok, frame, faces, time = fd.hasFace()
print ok
print frame
print faces
print time
if ok:
	print frame
	cv2.imshow('img', frame)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
