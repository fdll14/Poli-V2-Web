import os
from flask import ( render_template, url_for, request, redirect,  session, flash,  jsonify)
from numpy import histogram
from app import app
import json
from app.models.answererror import Answererror
from app.models.dataset import Dataset
from app.models.train import Train
from app.models.chatbot import Chatbot
from app.models.history import History


# ADMIN
@app.route('/admin', methods = ['GET'])
def admin():
    if not session.get('id'):
        return redirect(url_for('login'))
    else:
        dataset = Dataset()
        data = {
            'dataset':dataset.get()
        }
        return render_template('admin/index.html',data=data)

#dataset
@app.route('/admin/dataset/<idx>', methods = ['GET', 'POST'])
def dataset(idx='all'):
    if request.method == "POST":
        dataset = Dataset()
        inputan = request.form
        
        dataset.store(inputan['tag'],inputan['pattern'], inputan['response'], inputan['context'])
        flash('Berhasil tambah data')
        return redirect(url_for('admin', idx='all'))
    elif request.method == "GET" :
        if idx == 'all':
            dataset = Dataset()
            data = {
                'dataset':dataset.get()
            }
            return render_template('admin/index.html', data=data)
        else:
            dataset = Dataset()
            data = dataset.getOne(idx)
            return jsonify(result=data)

@app.route('/admin/dataset/get')
def get_dataset_json():
    dataset = Dataset()
    return jsonify(Chatbot.get_json())

@app.route('/admin/dataset/delete/<idx>', methods = ['GET'])
def admin_dataset_delete(idx=None):
    dataset = Dataset()
    data = dataset.destroy(idx)
    flash('Berhasil hapus data')

    return redirect(url_for('admin', idx='all'))

@app.route('/admin/dataset/update', methods = ['POST'])
def dataset_update():
    dataset = Dataset()
    inputan = request.form
    dataset.update(inputan['id'], inputan['tag'],inputan['pattern'], inputan['response'], inputan['context'])
    flash('Berhasil update data')
    return redirect(url_for('admin', idx='all'))

@app.route('/admin/dataset/train', methods = ['GET'])
def admin_dataset_train():
    f = open(r'D:\Poli\app\resources\intents.json', "w")
    dataset = Dataset()
    train = Train()
    jsonString = dataset.get_json()
    f.write(json.dumps(jsonString))
    f.close()
    train.train()
    flash('Train data selesai')
    return redirect(url_for('admin', idx='all'))

#answer error
@app.route('/admin/answer-error/<idx>', methods = ['GET', 'POST'])
def answer_error(idx='all'):
    if request.method == "POST":
        answererror = Answererror()
        inputan = request.form
        answererror.store(inputan['pertanyaan'], inputan['status'])
        flash('Berhasil tambah data')
        return redirect(url_for('answer_error', idx='all'))
    elif request.method == "GET" :
        if idx == 'all':
            answererror = Answererror()
            data = answererror.get()
            return render_template('admin/answer_error.html', data=data)
        else:
            answererror = Answererror()
            data = answererror.getOne(idx)
            return jsonify(result=data)
            
@app.route('/admin/answer-error/delete/<idx>', methods = ['GET'])
def answer_error_delete(idx=None):
    answererror = Answererror()
    data = answererror.destroy(idx)
    flash('Berhasil hapus data')
    return redirect(url_for('answer_error', idx='all'))

@app.route('/admin/answer-error/update', methods = ['POST'])
def answer_error_update():
    answererror = Answererror()
    inputan = request.form
    answererror.update(inputan['id'], inputan['pertanyaan'], inputan['status'])
    flash('Berhasil update data')
    return redirect(url_for('answer_error', idx='all'))

# HISTORY MOBILE
@app.route('/admin/history-mobile', methods = ['GET'])
def admin_history():
    history_mobile = History()
    data = history_mobile.get()
    return render_template('admin/history_mobile.html',data=data)
 