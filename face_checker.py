__author__ = 'Bhagat'
import cv2

def face_checker(img):
    face_csc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces_detect = face_csc.detectMultiScale(gray,1.1,4)
    face = False

    temp = img
    n=0
    faces = []

    for (x,y,w,h) in faces_detect:
        cv2.rectangle(temp, (x,y),(x+w,y+h),(0,255,0),3)
        face = True
        faces.append(temp.copy()[y:y+h,x:x+w])
    n = len(faces)
    return temp, faces, face, n