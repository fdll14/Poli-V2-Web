import cv2
import numpy as np
from keras.models import load_model
import os
import logging
from app import mysql
import time

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ['AUTOGRAPH_VERBOSITY'] = '0'
logging.getLogger('tensorflow').setLevel(logging.FATAL)


model=load_model(r'D:\Poli\trainingDataTarget\model-019.model')

video=cv2.VideoCapture(0)

faceDetect=cv2.CascadeClassifier(r'D:\Poli\app\resources\haarcascade_frontalface_default.xml')

color_dict={0: (0,0,255), 1: (0,255,0)}
labels_dict={0: "Female", 1: "Male"}

class Video(object):
    def __init__(self):
        self.video=cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()
    def get_frame(self):
        conn = mysql.connect()
        cursor = conn.cursor()
        ret,frame=self.video.read()
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray, 1.3, 5)
        for x,y,w,h in faces:
            x1,y1=x+w, y+h
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,255), 1)
            cv2.line(frame, (x,y), (x+30, y),(255,0,255), 6) #Top Left
            cv2.line(frame, (x,y), (x, y+30),(255,0,255), 6)

            cv2.line(frame, (x1,y), (x1-30, y),(255,0,255), 6) #Top Right
            cv2.line(frame, (x1,y), (x1, y+30),(255,0,255), 6)

            cv2.line(frame, (x,y1), (x+30, y1),(255,0,255), 6) #Bottom Left
            cv2.line(frame, (x,y1), (x, y1-30),(255,0,255), 6)

            cv2.line(frame, (x1,y1), (x1-30, y1),(255,0,255), 6) #Bottom right
            cv2.line(frame, (x1,y1), (x1, y1-30),(255,0,255), 6)
            sub_face_img=gray[y:y+h, x:x+w]
            resized=cv2.resize(sub_face_img,(32,32))
            normalize=resized/255.0
            reshaped=np.reshape(normalize, (1, 32, 32, 1))
            result=model.predict(reshaped)
            label=np.argmax(result, axis=1)[0]
            if label == 0:
                gender ="P"
                id ="1"
                print('Perempuan')
                # insert to db
                cursor.execute("UPDATE gender SET gender ='"+gender+"' WHERE id_gender = "+id)
                conn.commit()
            else:
                gender ="L"
                id ="1"
                print('Laki-laki')
                # insert to db
                cursor.execute("UPDATE gender SET gender ='"+gender+"' WHERE id_gender = "+id)
                conn.commit()
            cv2.rectangle(frame,(x,y-40),(x+w,y),color_dict[label],-1)
            cv2.putText(frame, labels_dict[label], (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
            time.sleep(10)
        ret,jpg=cv2.imencode('.jpg',frame)
        return jpg.tobytes()
        # time.sleep(30)

class Realtime(object):
    def __init__(self):
        self.video=cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()
    def get_frame(self):
        conn = mysql.connect()
        cursor = conn.cursor()
        ret,frame=self.video.read()
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray, 1.3, 5)
        for x,y,w,h in faces:
            x1,y1=x+w, y+h
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,255), 1)
            cv2.line(frame, (x,y), (x+30, y),(255,0,255), 6) #Top Left
            cv2.line(frame, (x,y), (x, y+30),(255,0,255), 6)

            cv2.line(frame, (x1,y), (x1-30, y),(255,0,255), 6) #Top Right
            cv2.line(frame, (x1,y), (x1, y+30),(255,0,255), 6)

            cv2.line(frame, (x,y1), (x+30, y1),(255,0,255), 6) #Bottom Left
            cv2.line(frame, (x,y1), (x, y1-30),(255,0,255), 6)

            cv2.line(frame, (x1,y1), (x1-30, y1),(255,0,255), 6) #Bottom right
            cv2.line(frame, (x1,y1), (x1, y1-30),(255,0,255), 6)
            sub_face_img=gray[y:y+h, x:x+w]
            resized=cv2.resize(sub_face_img,(32,32))
            normalize=resized/255.0
            reshaped=np.reshape(normalize, (1, 32, 32, 1))
            result=model.predict(reshaped)
            label=np.argmax(result, axis=1)[0]
            cv2.rectangle(frame,(x,y-40),(x+w,y),color_dict[label],-1)
            cv2.putText(frame, labels_dict[label], (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
        ret,jpg=cv2.imencode('.jpg',frame)
        return jpg.tobytes()
        # time.sleep(30)