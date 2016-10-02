import time

def seconds():
	return time.time() * 10000

howLong = 5 # in seconds
start = seconds()
while( (start + howLong) > seconds() ):
	print "waiting"
