__author__ = 'Bhagat'
import cv2
import time
import speech
import numpy as np
import os
from multiprocessing import Process
from emailer import email
from information import get_info
from face_checker import face_checker
from accessing_google_drive import update

file = open('armed.txt','w')
file.write('disarm')
file.close()

def security_cam(cam_num = 0):
    cam = cv2.VideoCapture(cam_num)
    while True:
        armed = False
        space = 0
        caught = False
        face = False
        finish = False
        face_frame = ''
        delete = []
        max = 0
        place=''

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fourcc2 = cv2.VideoWriter_fourcc(*'XVID')
        fourcc3 = cv2.VideoWriter_fourcc(*'XVID')
        vid  = cv2.VideoWriter('video_evidence.avi',fourcc,7, (640,480))
        vid2  = cv2.VideoWriter('face_video_evidence.avi',fourcc2,7, (640,480))
        vid3  = cv2.VideoWriter('difference_video_evidence.avi',fourcc3,7, (640,480))

        tf, frame = cam.read()

        old_frame = frame

        count = 0
        start = 0
        n = 0
        end = 0

        while True:
            tf, frame = cam.read()
            n+=1
            print armed, caught
            if not caught and tf:
                same = True
                counter = 0
                for x in range(len(frame)):
                    for y in range(len(frame[x])):
                        for z in range(len(frame[x][y])):
                            if not frame[x][y][z]-30<old_frame[x][y][z]<frame[x][y][z]+30:
                                counter+=1
                            if counter>200:
                                same=False
                                break
                        if not same:
                            break
                    if not same:
                        break
                if not same:
                    count+=1
                    if not armed:
                        pass
                else:
                    count = 0
                space+=1
                file = open('armed.txt')
                action = file.read()
                file.close()
                if action=='turn off':
                    finish= True
                    speech.say('goodbye')
                    break
                elif action=='arm' and not armed:
                    speech.say('You have 30 seconds until the camera is armed')
                    time.sleep(15)
                    speech.say('15 seconds')
                    time.sleep(10)
                    speech.say('5')
                    time.sleep(5)
                    speech.say('armed')
                    armed=True
                    space=0
                elif action=='disarm' and armed:
                    speech.say('disarmed')
                    armed = False
                    space=0
                if count>3 and armed and space>2:
                    caught = True
                    start = time.time()
                    delete.append('difference.jpg')
                    cv2.imwrite('difference.jpg',np.absolute(np.array(cv2.subtract(frame,old_frame))))
                    face_frame, faces, face, n = face_checker(frame.copy())
                    max = n
                    if face:
                        delete.append('face_picture.jpg')
                        cv2.imwrite('face_picture.jpg',face_frame)
                    for num in range(n):
                        delete.append('face'+str(num)+'.jpg')
                        cv2.imwrite('face'+str(num)+'.jpg',faces[num])
                    cv2.imwrite('motion_picture.jpg',frame)
                    delete.append('motion_picture.jpg')
                    current_time, place = get_info()

                go_arm = True
                if not armed:
                    for x in range(len(frame)):
                        for y in range(len(frame[x])):
                            for z in range(len(frame[x][y])):
                                if frame[x][y][z]>50:
                                    go_arm = False

                                if not go_arm:
                                    break
                            if not go_arm:
                                break
                        if not go_arm:
                            break
                if go_arm and not armed:
                    speech.say('You have 60 seconds until the camera is armed')
                    time.sleep(30)
                    speech.say('30 seconds')
                    time.sleep(15)
                    speech.say('15 seconds')
                    time.sleep(10)
                    speech.say('5')
                    time.sleep(5)
                    speech.say('armed')
                    armed=True
                    space = 0
                old_frame = frame
            else:
                end = time.time()
                face_frame,faces, face, n = face_checker(frame.copy())
                try:
                    file = open('face0.jpg')
                    file.close()
                    if n>max:
                        max = n
                        raise IOError
                except IOError:
                    if face:
                        delete.append('face_picture.jpg')
                        cv2.imwrite('face_picture.jpg',face_frame)
                    for num in range(n):
                        delete.append('face'+str(num)+'.jpg')
                        cv2.imwrite('face'+str(num)+'.jpg',faces[num])

                if face:
                    vid2.write(face_frame)
                else:
                    vid2.write(frame)
                vid.write(frame)
                vid3.write(np.absolute(np.array(cv2.subtract(frame,old_frame))))
                if end-start>=15:
                    break
                old_frame = frame
        vid.release()
        vid2.release()
        vid3.release()
        for b in delete:
            bob = False
            if b is not 'none':
                for a in range(len(delete)):
                    if delete[a]==b:
                        if bob:
                          delete[a]='none'
                        else:
                            bob = True
        if not finish:
            files = delete
            files.append('video_evidence.avi')
            files.append('difference_video_evidence.avi')
            if place is '':
                if 'face0.jpg' in delete:
                    files.append('face_video_evidence.avi')
                    if max==1:
                        string='a PERSON'
                    else:
                        string = str(max)+' PEOPLE'
                    email('Motion was detected by '+string+' on '+current_time,'MOTION DETECTED!!!!!',files=files)
                    os.remove('E:\Comp Sci\Python\Security_camera\\face_picture.jpg')
                else:
                    email('Motion was detected on '+current_time,'MOTION DETECTED!!!!!',files=files)
            else:
                if 'face0.jpg' in delete:
                    files.append('face_video_evidence.avi')
                    if max==1:
                        string='a PERSON'
                    else:
                        string = str(max)+' PEOPLE'
                    email('Motion was detected by '+string+' on '+current_time+' near '+place,'MOTION DETECTED!!!!!',files=files)
                    os.remove('E:\Comp Sci\Python\Security_camera\\face_picture.jpg')
                else:
                    email('Motion was detected on '+current_time+' near '+place,'MOTION DETECTED!!!!!',files=files)
            try:
                for string in delete:
                    if string is not 'none':
                        os.remove('E:\Comp Sci\Python\Security_camera\\'+string)
            except WindowsError:
                pass
        else:
            break
    cam.release()
    cv2.destroyAllWindows()
    #os.remove('E:\Comp Sci\Python\Security_camera\\video_evidence.avi')

if __name__ =='__main__':
    Process(target=security_cam).start()
    Process(target=update).start()