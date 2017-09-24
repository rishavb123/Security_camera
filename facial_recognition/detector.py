import cv2
import sqlite3

def getProfile(id):
    try:
        conn = sqlite3.connect('FaceBase.db')
        cmd = 'SELECT * FROM People WHERE ID='+str(id)
        cursor = conn.execute(cmd)
        profile=None
        for row in cursor:
            profile = row
        conn.close()
        return profile
    except sqlite3.OperationalError:
        return None
face_detect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
rec=cv2.face.LBPHFaceRecognizer_create()
rec.read('recognizer/trainingData.yml')

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_detect.detectMultiScale(gray,1.1,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        id,conf=rec.predict(gray[y:y+h,x:x+w])
        if conf>75:
            id='Unknown'
        print conf
        profile = getProfile(id)
        if profile != None:
            cv2.putText(img, str(id)+': '+str(profile[1]),(x,int(y+h+10)),font,1,(0,255,0),2)
            cv2.putText(img, str(profile[2]),(x,int(y+h+40)),font,1,(0,255,0),2)
            cv2.putText(img, str(profile[3]),(x,int(y+h+70)),font,1,(0,255,0),2)
        else:
            cv2.putText(img, str(id) ,(x,int(y+h+10)),font,1,(0,255,0),2)

    cv2.imshow("Face",img)
    if cv2.waitKey(1)==ord('q'):
        break