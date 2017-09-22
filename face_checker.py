__author__ = 'Bhagat'
import cv2
import random

def face_checker(img):
    face_csc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces_detect = face_csc.detectMultiScale(gray,random.randrange(10,20)/10.0,4)
    face = False

    temp = img
    faces = []

    for (x,y,w,h) in faces_detect:
        cv2.rectangle(temp, (x,y),(x+w,y+h),(0,255,0),3)
        face = True
        faces.append(temp.copy()[y:y+h,x:x+w])
    n = len(faces)
    return temp, faces, face, n