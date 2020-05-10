from flask import Flask, flash, request, redirect, url_for, render_template
import flask
import os
from werkzeug.utils import secure_filename
from os import listdir
from os.path import isfile, join
import json
import face_recognition


app = flask.Flask(__name__)
app.debug = True
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


ALLOWED_EXTENSIONS = {'jpg'}

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/listar', methods=['GET'])
def listar():
    mypath ='faces'
    data = {}
    i = 0
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for files in onlyfiles:
        files = files.replace('.jpg','')
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
            flash('No file part')
            return redirect(request.url)
        arquivo = request.files['file']
        if arquivo.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if arquivo and allowed_file(arquivo.filename):
            filename = secure_filename(arquivo.filename)
            arquivo.save(os.path.join('faces/', filename))
            return 'Arquivo armazenado!'
            
    return render_template('armazenar.html')

@app.route('/comparar', methods=['GET', 'POST'])
def comparar_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        arquivo = request.files['file']
        if arquivo.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if arquivo and allowed_file(arquivo.filename):
            filename = secure_filename(arquivo.filename)
            arquivo.save(os.path.join('comparar/', filename))
            imgd = face_recognition.load_image_file('comparar/'+filename)
            faced = face_recognition.face_encodings(imgd)[0]
            imgcs = listar()
            resultado = {}
            for key, value in imgcs.items():
                imgc = face_recognition.load_image_file('faces/'+value+'.jpg')
                facec = face_recognition.face_encodings(imgc)[0]
                results = face_recognition.compare_faces([facec],faced)
                resultado.update({value:results})
            return str(resultado)
            
    return render_template('comparar.html')


app.run()
