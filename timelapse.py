#!/usr/bin/env python

import time
import picamera
import os, sys

def write_image():

	camera = picamera.PiCamera()
	camera.resolution = (2592,1944)
	
	cmd = 'ls /media/pi'
	ls = os.popen(cmd).read()
	drives = ls.split('\n')
	
	if len(drives) > 0:
		for drive in drives:
			if len(drive) < 1:
				continue
			path = os.path.join('/media/pi', drive)
			image_path = os.path.join(path, 'images')
			if not os.path.exists(image_path):
				os.mkdir(image_path)
		
			image_name = time.strftime('%Y%m%d_%H%M%S.jpg', time.gmtime())
			image_name_with_path = os.path.join(image_path, image_name)
			camera.capture(image_name_with_path)
			camera.close()

	else:
		print 'No media device!'
	
if __name__ == '__main__':
	dt = 10
	while 1:
		write_image()
		time.sleep(dt)
		
		
		