__author__ = 'Bhagat'
import os
import sqlite3
import cv2
import numpy as np
from PIL import Image



recog = cv2.face.LBPHFaceRecognizer_create()


path = 'dataSet'

file = open('sampleNum.txt')
start = int(file.read())
file.close()

file = open('ID.txt')
Id = int(file.read())
file.close()
def getImagesWithID(path,start,Id):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    print 'Machine got new photos'
    faces = []
    IDs = []
    for imagePath in imagePaths:
        if int(os.path.split(imagePath)[-1].split('.')[2])>start and Id==int(os.path.split(imagePath)[-1].split('.')[1]):
            faceImg = Image.open(imagePath).convert('L')
            faceNp = np.array(faceImg,'uint8')
            ID = int(os.path.split(imagePath)[-1].split('.')[1])
            faces.append(faceNp)
            IDs.append(ID)
    print 'Machine learned new photos'
    return np.array(IDs),faces

Ids,faces = getImagesWithID(path,start,Id)
if os.path.exists("recognizer/trainingData.yml"):
    recog.read("recognizer/trainingData.yml")
    print 'Machine read previous training'
    recog.update(faces,Ids)
else:
    recog.train(faces,Ids)
print 'Machine saved new training'
recog.write('recognizer/trainingData.yml')
