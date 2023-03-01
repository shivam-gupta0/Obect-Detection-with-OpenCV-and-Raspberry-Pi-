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
    
    def detect_car(self, img):
        car_l1 = 0

        
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        red = [[0,15,7], [22,255,149]]
	black = [[37, 0, 0], [255, 255, 51]]
        yellow = [[26, 117, 59], [255, 255, 244]]
        porche = [[89, 42, 21], [255, 104, 206]]
        popti = [[72, 56, 143], [81, 184, 225]]

        mask_r = cv2.inRange(img_hsv, np.array(red[0]), np.array(red[1]))
        mask_b = cv2.inRange(imgHSV, np.array(black[0]), np.array(black[1]))
        mask_y = cv2.inRange(imgHSV, np.array(yellow[0]), np.array(yellow[1]))
        mask_pr = cv2.inRange(imgHSV, np.array(porche[0]), np.array(porche[1]))
        mask_pp = cv2.inRange(imgHSV, np.array(popti[0]), np.array(popti[1]))

        image_r = cv2.bitwise_and(img, img, mask=mask_r)
        image_b = cv2.bitwise_and(im, im, mask=mask_b)
        image_y = cv2.bitwise_and(im, im, mask=mask_y)
        image_pr = cv2.bitwise_and(im, im, mask=mask_pr)
        image_pp = cv2.bitwise_and(im, im, mask=mask_pp)

        img_arr_r = asarray(image_r)
        img_arr_b = asarray(image_b)
        img_arr_y = asarray(image_y)
        img_arr_pr = asarray(image_pr)
        img_arr_pp = asarray(image_pp)

        img_r_data = np.asarray(img_arr_r)
        img_b_data = asarray(img_arr_b)
        img_y_data = asarray(img_arr_y)
        img_pr_data = asarray(img_arr_pr)
        img_pp_data = asarray(img_arr_pp)

        count_r = np.count_nonzero(img_r_data)
        count_b = np.count_nonzero(img_b_data)
        count_y = np.count_nonzero(img_y_data)
        count_pr = np.count_nonzero(img_pr_data)
        count_pp = np.count_nonzero(img_pp_data)


        if count_r > 20000:
            cnts = cv2.findContours(mask_r.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            if len(cnts) > 0:
                blue_area = max(cnts, key=cv2.contourArea)
                (xg, yg, wg, hg) = cv2.boundingRect(blue_area)
                cv2.rectangle(img, (xg, yg), (xg + wg, yg + hg), (0, 255, 0), 1)
                cv2.putText(img, "car", (xg, yg), self.font, 5, (255, 255, 0), 3)
                car_l1 = 1

	 if count_b > 20000:
            cnts = cv2.findContours(mask_b.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            if len(cnts) > 0:
                blue_area = max(cnts, key=cv2.contourArea)
                (xg, yg, wg, hg) = cv2.boundingRect(blue_area)
                cv2.rectangle(im, (xg, yg), (xg + wg, yg + hg), (0, 255, 0), 1)
                cv2.putText(im, "car", (xg, yg), font, 5, (255, 255, 0), 3)
        
        if count_y > 20000:
            cnts = cv2.findContours(mask_y.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            if len(cnts) > 0:
                blue_area = max(cnts, key=cv2.contourArea)
                (xg, yg, wg, hg) = cv2.boundingRect(blue_area)
                cv2.rectangle(im, (xg, yg), (xg + wg, yg + hg), (0, 255, 0), 1)
                cv2.putText(im, "car", (xg, yg), font, 5, (255, 255, 0), 3)
                car_l1 = 1
                
        
        if count_pr > 15000:
            cnts = cv2.findContours(mask_pr.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            if len(cnts) > 0:
                blue_area = max(cnts, key=cv2.contourArea)
                (xg, yg, wg, hg) = cv2.boundingRect(blue_area)
                cv2.rectangle(im, (xg, yg), (xg + wg, yg + hg), (0, 255, 0), 1)
                cv2.putText(im, "car", (xg, yg), font, 5, (255, 255, 0), 3)
                car_l1 = 1

        if count_pp > 20000:
            cnts = cv2.findContours(mask_pp.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            if len(cnts) > 0:
                blue_area = max(cnts, key=cv2.contourArea)
                (xg, yg, wg, hg) = cv2.boundingRect(blue_area)
                cv2.rectangle(im, (xg, yg), (xg + wg, yg + hg), (0, 255, 0), 1)
                cv2.putText(im, "car", (xg, yg), font, 5, (255, 255, 0), 3)
                car_l1 = 1

        return car_l1
    
    def run(self):
        for frame in self.camera.capture_continuous(self.raw_capture, format="bgr", use_video_port=True):
            car_l1 = 0


            img = frame.array
            car_l1 = self.detect_car(img)

            if car_l1 > 0 and (self.phase == 0 or self.phase == 1) :
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
