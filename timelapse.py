#!/usr/bin/env python

import time
import picamera
import picamera.array
import os, sys
import numpy as np

def calculate_shutter_speed(camera, initial_shutter_speed, desired_median):
        actual_median = 0
        shutter_speed = initial_shutter_speed
        gain = -10

        with picamera.array.PiRGBArray(camera) as stream:
                camera.exposure_mode = 'night'
		camera.exposure_compensation = 10
                camera.resolution = (320, 240)
                camera.shutter_speed = shutter_speed
                camera.iso = 800
		print 'starting auto exposure routine'
                camera.framerate = 3
                print 'letting digital and analog gains settle'
                #while camera.digital_gain == 0:
                time.sleep(5)         
                print camera.digital_gain, camera.analog_gain   
                camera.shutter_speed = shutter_speed
                camera.exposure_mode = 'off'

                iterations = 0
                while np.abs(actual_median - desired_median) > 5:
                    camera.capture(stream, 'bgr', use_video_port=True)
                    # stream.array now contains the image data in BGR order
                    # reset the stream before the next capture


                    actual_median = np.median(stream.array)
		    err = actual_median - desired_median
                    shutter_speed = int(shutter_speed + gain*(err))  
                    print err, shutter_speed          
                    #if np.abs(shutter_speed - camera.shutter_speed) < 40:
		    #    if err < 20:
                    #        camera.iso = camera.iso*2
                    camera.shutter_speed = shutter_speed
                    print actual_median, camera.shutter_speed, camera.exposure_speed, camera.iso


                    stream.seek(0)
                    stream.truncate()
                
                    iterations += 1
                    if iterations > 100:
                        break

	return camera, shutter_speed

def write_image(camera):

	camera.resolution = (2592,1944)

	path = '/media/usb'
	image_path = os.path.join(path, 'images')
	if not os.path.exists(image_path):
		os.mkdir(image_path)

	image_name = time.strftime('%Y%m%d_%H%M%S.jpg', time.gmtime())
	image_name_with_path = os.path.join(image_path, image_name)
	camera.capture(image_name_with_path)

if __name__ == '__main__':
	dt = 10
	shutter_speed = 30000 # initial
	desired_median = 220
	while 1:
		tstart = time.time()
                with picamera.PiCamera() as camera:
                        print 'starting shutter speed: ', shutter_speed
                        camera, shutter_speed = calculate_shutter_speed(camera, shutter_speed, desired_median)
               		write_image(camera)
                telapsed = time.time() - tstart

		if telapsed < dt:
			time.sleep(dt-telapsed)
		
		
		
