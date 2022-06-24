from app import app
from flask_restful import Resource
import pickle
from tensorflow.keras.models import load_model
from flask import Flask, jsonify,request,flash
from itsdangerous import json
from werkzeug.utils import secure_filename
import keras
from keras.models import Sequential
from keras.layers import Dense,Conv2D,MaxPool2D,Dropout,BatchNormalization,Flatten,Activation
from keras.preprocessing import image 
from keras.preprocessing.image import ImageDataGenerator
from PIL import Image
from keras.utils.vis_utils import plot_model
import numpy as np
import os
from app import mysql


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
MODEL_PATH = r'D:\Poli\app\resources\model_fix.h5'
model = load_model(MODEL_PATH,compile=False)

pickle_inn = open(r'D:\Poli\app\resources\num_class_gender.pkl','rb')
num_classes_bird = pickle.load(pickle_inn)

def allowed_file(filename):     
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

 

class gender(Resource):
  def post(self):
    conn = mysql.connect()
    cursor = conn.cursor()
    if 'image' not in request.files:
      flash('No file part')
      return jsonify({
            "pesan":"tidak ada form image"
          })
    file = request.files['image']
    if file.filename == '':
      return jsonify({
            "pesan":"tidak ada file image yang dipilih"
          })
    if file and allowed_file(file.filename):
      path_del = r'D:\Poli\app\static\upload\fotogender\\'
      for file_name in os.listdir(path_del):
        # construct full file path
        file_del = path_del + file_name
        if os.path.isfile(file_del):
            print('Deleting file:', file_del)
            os.remove(file_del)
            print("file "+file_del+" telah terhapus")
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      path=(r'D:\Poli\app\static\upload\fotogender\\'+filename)

      #def predict(dir):
      img=keras.utils.load_img(path,target_size=(224,224))
      img1=keras.utils.img_to_array(img)
      img1=img1/255
      img1=np.expand_dims(img1,[0])
      # plt.imshow(img)
      predict=model.predict(img1)
      classes=np.argmax(predict,axis=1)
      for key,values in num_classes_bird.items():
          if classes==values:
            accuracy = float(round(np.max(model.predict(img1))*100,2))
 
            if accuracy >75:
              print("hasil prediksi jenis_kelamin : "+str(key)+" with a probability of "+str(accuracy)+"%")
              cursor.execute("INSERT INTO history_mobile (hasil_gender, akurasi,foto) VALUES (%s, %s, %s)", (key, accuracy, filename))
              conn.commit()
              return jsonify({
                "gender":str(key),
                "Accuracy":str(accuracy)+"%",
              })
            else :
              print("The predicted image of the gender is: "+str(key)+" with a probability of "+str(accuracy)+"%")
              return jsonify({
                "Message":str("Jenis kelamin tidak terdeteksi"),
                "Accuracy":str(accuracy)+"%"               
                
              })
      
    else:
      return jsonify({
        "Message":"bukan file image"
      })

