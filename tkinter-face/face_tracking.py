# USAGE
# python face_tracking.py --video object_tracking_example.mp4
# python face_tracking.py
# Attribution: Adrian Rosebrock on September 21, 2015
# https://www.pyimagesearch.com/2015/09/21/opencv-track-object-movement/

# import the necessary packages
from collections import deque
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
	help="max buffer size")
args = vars(ap.parse_args())

# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()

	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break
	#loads face cascade
	#finds faces in stream
	#draws a rectangle & locate center
	font = cv2.FONT_HERSHEY_SIMPLEX
	frame = cv2.flip(frame, 1)
	height, width, channels = frame.shape 
	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
	frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(frame_gray, 1.3, 5)
	for (x,y,w,h) in faces:
		face_center = int(x+w/2), int(y+h/3)
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
		cv2.circle(frame, face_center, 5, (0, 0, 255), -1)
		cv2.putText(frame,'x: {0} | y: {1}'.format(face_center[0], face_center[1]),(10,50), font, 1.2,(0,0,255),1)
		if len(pts) > 10:
			x_diff = face_center[0] - pts[-5][0]
			y_diff = face_center[1] - pts[-5][1]
			if abs(x_diff) > 20:
				cv2.putText(frame,'Head Shake',(20,height//2), font, 1.2,(0,0,255),1)
			if abs(y_diff) > 20:
				cv2.putText(frame,'Head Nod!',(20,height//2), font, 1.2,(0,0,255),1)
			cv2.putText(frame,'dx: {0} | dy: {1}'.format(x_diff, y_diff),(10,height-50), font, 1.2,(0,0,255),1)
		pts.append(face_center)

	cv2.imshow('Video', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
