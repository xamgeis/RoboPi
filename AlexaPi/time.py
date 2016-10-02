import time
import cv2

def seconds():
	return time.time()

howLong = 5 # in seconds
start = seconds()
print "start: " , start
print "end: " , (start+howLong)

while( (start + howLong) > seconds() ):
	
	key = cv2.waitKey()
	if key == ord('a'):
		print key
		break
