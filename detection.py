from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
import numpy as np
import serial
import time


class TrafficLightSystem:
    def __init__(self, camera_resolution=(720, 480), camera_framerate=32):
        self.camera = PiCamera()
        self.camera.resolution = camera_resolution
        self.camera.framerate = camera_framerate
        self.raw_capture = PiRGBArray(self.camera, size=camera_resolution)
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.phase = 0
        self.arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        time.sleep(2)
    
    def detect_car(self, img, color_range, label):
        car_l1 = 0
        
        mask = cv2.inRange(img, np.array(color_range[0]), np.array(color_range[1]))
        img_filtered = cv2.bitwise_and(img, img, mask=mask)
        
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.putText(img, label, (x, y), self.font, 5, (255, 255, 0), 3)
            car_l1 = 1

        return car_l1
    
    def run(self):
        for frame in self.camera.capture_continuous(self.raw_capture, format="bgr", use_video_port=True):
            car_l1 = 0
            img = frame.array

            color_ranges = {
                'red': [[0, 15, 7], [22, 255, 149]],
                'black': [[37, 0, 0], [255, 255, 51]],
                'yellow': [[26, 117, 59], [255, 255, 244]],
                'porche': [[89, 42, 21], [255, 104, 206]],
                'popti': [[72, 56, 143], [81, 184, 225]]
            }

            for color, range in color_ranges.items():
                if np.count_nonzero(cv2.inRange(img, np.array(range[0]), np.array(range[1]))) > 20000:
                    car_l1 = self.detect_car(img, range, 'car')
                    break

            if car_l1 > 0 and (self.phase == 0 or self.phase == 1):
                self.arduino.write("is1".encode())
                response = str(self.arduino.readline())
                if len(response) > 4:
			strng = response[2:10]
			time.sleep(0.2)
	     if car_l2 > 0 and strng == "is1 done":
			self.phase = 2
			print(self.phase)
	     elif car_l2 == 0 and strng == "is1 done":
			print("no red")
			self.phase = 0
			cv2.imshow("frame", img)
              key = cv2.waitKey(1) & 0xFF
              self.raw_capture.truncate(0)
              if key == ord("q"):
              	 break
