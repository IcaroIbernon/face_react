from flask import Flask, flash, request, redirect, url_for
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
    return "<h1>Sistema de Reconhecimento Facial</h1><p>Projeto inicial de um sistema de reconhecimento facil.</p>"

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
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        arquivo = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if arquivo.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if arquivo and allowed_file(arquivo.filename):
            filename = secure_filename(arquivo.filename)
            arquivo.save(os.path.join('faces/', filename))
            return 'arquivo armazenado'
            
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/comparar', methods=['GET', 'POST'])
def comparar_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        arquivo = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
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
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

app.run()
