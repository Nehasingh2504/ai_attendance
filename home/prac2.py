import cv2
import os
import face_recognition
import warnings
import pickle
warnings.filterwarnings("ignore", category=UserWarning, module="face_recognition_models")

def detect_stu():
    folderpath = 'C:/Users/PC/Desktop/CS/ai attendance/project/student/class_3'
    file = os.listdir(folderpath)
    encodedlist = []

    for img in file:
        print('img',img)
        img =  cv2.cvtColor(cv2.imread(os.path.join(folderpath,img)),cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodedlist.append(encode)

    print(encodedlist)
    
print('start')
detect_stu()
print('end')