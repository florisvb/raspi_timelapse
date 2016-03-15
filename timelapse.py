#!/usr/bin/env python

import time
import picamera
import os, sys

def write_image():

	camera = picamera.PiCamera()
	camera.resolution = (2592,1944)

	path = '/media/usb'
	image_path = os.path.join(path, 'images')
	if not os.path.exists(image_path):
		os.mkdir(image_path)

	image_name = time.strftime('%Y%m%d_%H%M%S.jpg', time.gmtime())
	image_name_with_path = os.path.join(image_path, image_name)
	camera.capture(image_name_with_path)
	camera.close()
	
if __name__ == '__main__':
	dt = 10
	while 1:
		write_image()
		time.sleep(dt)
		
		
		