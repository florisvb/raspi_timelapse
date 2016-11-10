#!/usr/bin/env python

import time
import picamera
import picamera.array
import os, sys
import numpy as np
import atexit, signal
import RPi.GPIO as GPIO

class Timelapse():
    def __init__(self):
        self.is_shutdown = False
        atexit.register(self.release)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
    def calculate_exposure_compensation(self):
        camera = self.camera
        exposure_compensation = self.exposure_compensation
        desired_median = self.desired_median
        
        actual_median = 0
        gain = -0.01
        
        with picamera.array.PiRGBArray(camera) as stream:
            camera.exposure_compensation = int(exposure_compensation)
            camera.resolution = (320, 240)
            camera.framerate = 3
            time.sleep(5)
            
            iterations = 0
            while np.abs(actual_median - desired_median) > 5:
                camera.capture(stream, 'bgr', use_video_port=True)
                # stream.array now contains the image data in BGR order
                # reset the stream before the next capture


                actual_median = np.median(stream.array[110:-110,150:-150])
                err = actual_median - desired_median
                float_ec = exposure_compensation + gain*(err)
                exposure_compensation = float_ec
                done = False
                if exposure_compensation > 25:
                    exposure_compensation = 25
                    done = True
                if exposure_compensation < -25:
                    exposure_compensation = -25
                    done = True
                #print err, float_ec, exposure_compensation, camera.exposure_compensation
                #if np.abs(shutter_speed - camera.shutter_speed) < 40:
                #    if err < 20:
                #        camera.iso = camera.iso*2
                if camera.exposure_compensation == exposure_compensation:
                    done = True
                camera.exposure_compensation = int(exposure_compensation)
                #print actual_median, camera.exposure_compensation, camera.exposure_speed

                stream.seek(0)
                stream.truncate()
            
                iterations += 1
                if iterations > 100 or done:
                    break

	    self.exposure_compensation = exposure_compensation

    def write_image(self):
        camera = self.camera
        
	camera.resolution = (2592,1944)
	#camera.resolution = (320,240)

	path = '/media/usb'
	image_path = os.path.join(path, 'images')
	if not os.path.exists(image_path):
	    os.mkdir(image_path)

	image_name = time.strftime('%Y%m%d_%H%M%S.jpg', time.gmtime())
	image_name_with_path = os.path.join(image_path, image_name)
	camera.capture(image_name_with_path)
	    
    def run_timelapse(self, dt=10, desired_median=200, exposure_compensation=10):
	
	self.exposure_compensation = exposure_compensation
	self.desired_median = desired_median
		
        with picamera.PiCamera() as self.camera:
            self.camera.exposure_mode = 'night'
            self.camera.awb = 'off'
            self.camera.awb_gains = (1.5, 1.2)
            self.camera.shutter_speed = 0
                            
            while not self.is_shutdown:
		tstart = time.time()
                self.calculate_exposure_compensation()
		print 'calculated exposure'
           	self.write_image()
		print 'wrote image'		
                telapsed = time.time() - tstart
		print 'sleeping'
		if telapsed < dt:
		    time.sleep(dt-telapsed)
                print 'awake'

		gpio_pin_21 = GPIO.input(21)
		if not gpio_pin_21:
			self.release()
			sys.exit(0)
                #try:
                #    GPIO.wait_for_edge(21, GPIO.FALLING)
		#    
                #    self.release()
                #except:
                #    pass

    def release(self):
        self.is_shutdown = True
        self.camera.close()
        print 'released resources'

    def signal_handler(signol, frame):
        print 'shutting down'
        sys.exit(0)

if __name__ == '__main__':
    time.sleep(1)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	
    timelapse = Timelapse()
    timelapse.run_timelapse()
		
		
