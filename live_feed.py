__author__ = 'Bhagat'
import cv2
import time


def liveFeed():
    x=0
    cam = cv2.VideoCapture(0)
    while True:
        start = time.time()
        tf, frame = cam.read()
        if x>=100:
            x=0
        x+=1
        cv2.imwrite('Live_feed_images\web_image'+str(x)+'.jpg',frame)
        print time.time()-start
liveFeed()