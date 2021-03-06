from flask import Flask, flash, request, redirect, url_for, render_template
import flask
import os
from werkzeug.utils import secure_filename
from os import listdir
from os.path import isfile, join
import json
import face_recognition
import numpy as np

app = flask.Flask(__name__)
app.debug = True
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


ALLOWED_EXTENSIONS = {'jpg'}

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/listar', methods=['GET'])
def listar(nomes = None):
    mypath ='faces'
    data = []
    i = 0
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for files in onlyfiles:
        files = files.replace('.npy','')
        data.append(files)
    return render_template('lista.html', nomes = data)

def listar2():
    mypath ='faces'
    data = {}
    i = 0
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for files in onlyfiles:
        files = files.replace('.npy','')
        data.update({i:files})
        i = i+1
    return data

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/armazenar', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        arquivo = request.files['file']
        if arquivo.filename == '':
            return redirect(request.url)
        if arquivo and allowed_file(arquivo.filename):
            filename = secure_filename(arquivo.filename)
            known_image = face_recognition.load_image_file(arquivo)
            know_encoding = face_recognition.face_encodings(known_image)[0]
            filename = filename.replace('jpg','npy')
            np.save(os.path.join('faces/', filename),know_encoding)
            return render_template('armazenado.html')
            
    return render_template('armazenar.html')

@app.route('/comparar', methods=['GET', 'POST'])
def comparar_file(nome = None):
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        arquivo = request.files['file']
        if arquivo.filename == '':
            return redirect(request.url)
        if arquivo and allowed_file(arquivo.filename):
            filename = secure_filename(arquivo.filename)
            imgd = face_recognition.load_image_file(arquivo)
            faced = face_recognition.face_encodings(imgd)[0]
            imgcs = listar2()
            for key, value in imgcs.items():
                facec = np.load('faces/'+value+'.npy')
                results = face_recognition.compare_faces([facec],faced)
                if (results[0] == True):
                    return render_template('confirmado.html', nome = value)
            return render_template('negado.html')
            
    return render_template('comparar.html')


app.run()
