from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
from time import sleep
import numpy as np
from numpy import asarray
import serial
import time


camera = PiCamera()
camera.resolution = (720,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(720,480))
font = cv2.FONT_HERSHEY_PLAIN

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        car_l1 = 0
        car_l2 = 0
        

        im = frame.array
        imgHSV = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        red = [[0,15,7], [22,255,149]]
        black = [[37, 0, 0], [255, 255, 51]]
        yellow = [[26, 117, 59], [255, 255, 244]]
        porche = [[89, 42, 21], [255, 104, 206]]
        popti = [[72, 56, 143], [81, 184, 225]]
    
        mask_r = cv2.inRange(imgHSV, np.array(red[0]), np.array(red[1]))
        mask_b = cv2.inRange(imgHSV, np.array(black[0]), np.array(black[1]))
        mask_y = cv2.inRange(imgHSV, np.array(yellow[0]), np.array(yellow[1]))
        mask_pr = cv2.inRange(imgHSV, np.array(porche[0]), np.array(porche[1]))
        mask_pp = cv2.inRange(imgHSV, np.array(popti[0]), np.array(popti[1]))

        image_r = cv2.bitwise_and(im, im, mask=mask_r)
        image_b = cv2.bitwise_and(im, im, mask=mask_b)
        image_y = cv2.bitwise_and(im, im, mask=mask_y)
        image_pr = cv2.bitwise_and(im, im, mask=mask_pr)
        image_pp = cv2.bitwise_and(im, im, mask=mask_pp)

        img_arr_r = asarray(image_r)
        img_arr_b = asarray(image_b)
        img_arr_y = asarray(image_y)
        img_arr_pr = asarray(image_pr)
        img_arr_pp = asarray(image_pp)

        img_r_data = asarray(img_arr_r)
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
                cv2.rectangle(im, (xg, yg), (xg + wg, yg + hg), (0, 255, 0), 1)
                cv2.putText(im, "car", (xg, yg), font, 5, (255, 255, 0), 3)
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
                car_ln1 = 1

        if count_pp > 20000:
            cnts = cv2.findContours(mask_pp.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            if len(cnts) > 0:
                blue_area = max(cnts, key=cv2.contourArea)
                (xg, yg, wg, hg) = cv2.boundingRect(blue_area)
                cv2.rectangle(im, (xg, yg), (xg + wg, yg + hg), (0, 255, 0), 1)
                cv2.putText(im, "car", (xg, yg), font, 5, (255, 255, 0), 3)
                car_l1 = 1
        
        if car_l1 > 0 and (phase == 0 or phase == 1) :
            arduino.write("is1".encode())
            response = str(arduino.readline())
            if len(response) > 4:
                strng = response[2:10]
                
            #response = str(arduino.readline())
                #print("TRAFFIC LIGHT Lane 1: {}".format(response))
            time.sleep(0.2)
            if car_l2 > 0 and strng == "is1 done":
                phase = 2
                print(phase)
            elif car_l2 == 0 and strng == "is1 done":
                print("no red")
                phase = 0
        
        if car_l2 > 0 and (phase == 0 or phase == 2):
            arduino.write("is2".encode())
            response = str(arduino.readline())
            if len(response) > 4:
                strng = response[2:10]
                #print("TRAFFIC LIGHT Lane 2: {}".format(response))
            time.sleep(0.2)
            if car_l1 > 0 and strng == "is2 done":
                phase = 1
                print(phase)
            elif car_l1 == 0 and strng == "is2 done":
                phase = 0
        
        cv2.imshow("frame",im)
    
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if key == ord("q"):
            break
