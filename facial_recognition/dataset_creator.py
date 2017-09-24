import cv2
import sqlite3
from encoder import decode

if raw_input('Password: ')!=decode('mwj%w|xfhfxit%xu'):
    raise Exception('Get the hell out')


def insertOrUpdate(Id,name,age,gender):
    conn = sqlite3.connect('FaceBase.db')
    cmd = 'SELECT * FROM People WHERE ID='+str(Id)
    cursor = conn.execute(cmd)
    exist = False
    for row in cursor:
        exist = True
    if exist:
        cmd = 'UPDATE People SET Name='+str(name)+' WHERE ID='+str(Id)
        conn.execute(cmd)
        if age!='':
            cmd = 'UPDATE People SET Age='+str(age)+' WHERE ID='+str(Id)
            conn.execute(cmd)
        if gender!='':
            cmd = 'UPDATE People SET Sex='+str(gender)+' WHERE ID='+str(Id)
            conn.execute(cmd)
    else:
        if age=='':
            age=0
        if gender=='':
            gender='Unknown'
        cmd="INSERT INTO People(ID,Name,Age,Sex) Values("+str(Id)+','+str(name)+','+str(age)+','+str(gender)+')'
        conn.execute(cmd)
    conn.commit()
    conn.close()

again=True
id = 0
while again:
    again=False
    try:
        id = raw_input("Enter User ID: ")
        if int(id)==0:
            file = open('idNum.txt')
            id = int(file.read())
            exist = True
            conn = sqlite3.connect('FaceBase.db')
            while exist:
                id+=1
                exist = False
                cmd = 'SELECT * FROM People WHERE ID='+str(id)
                cursor = conn.execute(cmd)
                exist = False
                for row in cursor:
                    exist = True
            conn.close()
            print 'You\'re ID is '+str(id)
            id = str(id)
            file.close()
            file = open('idNum.txt','w')
            file.write(str(int(id)))
            file.close()
    except ValueError:
        again=True
name ='\"'+raw_input("Name: ")+'\"'
age = raw_input('Age: ')
gender = '"'+raw_input("Gender: ")+'"'
samples = int(raw_input('Number of Samples: '))
if samples == 0:
    samples = float('inf')
insertOrUpdate(id,name,age,gender)

face_detect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)
def setSampleNum(id):
    conn = sqlite3.connect('SamplesBase.db')
    cmd = 'SELECT * FROM SampleNum WHERE ID='+str(id)
    cursor = conn.execute(cmd)
    total_samples=(id,0)
    for row in cursor:
        total_samples = row
    conn.close()
    return total_samples
sampleNum = start = int(setSampleNum(id)[1])
file = open('sampleNum.txt','w')
file.write(str(start))
file.close()
file = open('ID.txt','w')
file.write(str(id))
file.close()

def putInSampleNum(Id,sampleNum):
    conn = sqlite3.connect('SamplesBase.db')
    cmd = 'SELECT * FROM SampleNum WHERE ID='+str(Id)
    cursor = conn.execute(cmd)
    exist = False
    for row in cursor:
        exist = True
    if exist:
        cmd = 'UPDATE SampleNum SET Sample='+str(sampleNum)+' WHERE ID='+str(Id)
        conn.execute(cmd)
    else:
        cmd="INSERT INTO SampleNum(Sample) Values("+str(sampleNum)+')'
        conn.execute(cmd)
    conn.commit()
    conn.close()

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_detect.detectMultiScale(gray,1.3,5)
    for(x,y,w,h) in faces:
        sampleNum+=1
        print sampleNum
        cv2.imwrite('dataSet/User.'+str(id)+'.'+str(sampleNum)+'.jpg',gray.copy()[y:y+h,x:x+w])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.waitKey(100)
    cv2.imshow("Face",img)
    if cv2.waitKey(1)==ord('q'):
        break
    if sampleNum-start>=samples:
        break
print 'Machine is learning the new photos . . .'

putInSampleNum(id,sampleNum)

cam.release()
cv2.destroyAllWindows()
import trainer