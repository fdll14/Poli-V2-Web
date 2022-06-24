from app import app
from flask import ( render_template,  request,  Response)
import random
import numpy as np
import pickle
import json
from app.models.answererror import Answererror
import nltk
from keras.models import load_model
from nltk.stem import WordNetLemmatizer
from app.models.camera import Video
from app.models.gender import Gender 

lemmatizer = WordNetLemmatizer()

model = load_model(r'D:\Poli\app\resources\chatbot_model.h5')
intents = json.loads(open(r'D:\Poli\app\resources\intents.json').read())
words = pickle.load(open(r'D:\Poli\app\resources\words.pkl', "rb"))
classes = pickle.load(open(r'D:\Poli\app\resources\classes.pkl', "rb"))


@app.route("/bot")
def chatbot():
    return render_template("bot.html")
    
@app.route('/bot/get')
def get_gender():
    gender = Gender()
    data = {
		'gender': gender.getOne()
	}
    return data
            


@app.route("/get")
def chatbot_response():
    gender = request.args.get('gender')
    msg = request.args.get('msg')
    print(gender)
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    if gender == 'P':
        if msg == 'selamat pagi' or msg == 'pagi' or msg == 'selamat sore' or msg == 'sore' or msg ==  'selamat siang' or msg == 'siang' or msg == 'selamat malam' or msg == 'malam':
            return res + ' mba'
        else:
            if res == '':
                answererror = Answererror()
                inputan = msg
                status = "belum diperbaiki"
                answererror.store(inputan, status)
                return "maaf poli tidak mengerti"
            else:
                return res
    else:
        if msg == 'selamat pagi' or msg == 'pagi' or msg == 'selamat sore' or msg == 'sore' or msg == 'selamat siang' or msg == 'siang' or msg == 'selamat malam' or msg == 'malam':
            return res + ' mas'
        else:
            if res == '':
                answererror = Answererror()
                inputan = msg
                status = "belum diperbaiki"
                answererror.store(inputan, status)
                return "maaf poli tidak mengerti"
            else:
                return res


# chat functionalities
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i["responses"])
            break
    return result

# gender
def gen(camera):
    while True:
        frame=camera.get_frame()
        yield(b'--frame\r\n'
       b'Content-Type:  image/jpeg\r\n\r\n' + frame +
         b'\r\n\r\n')

@app.route('/video')
def video():
    return Response(gen(Video()),
    mimetype='multipart/x-mixed-replace; boundary=frame')