import face_recognition
import numpy

nome = 'Cris Rock'

imgd = face_recognition.load_image_file("Rock2.jpg")
faced = face_recognition.face_encodings(imgd)[0]
imgc = face_recognition.load_image_file('faces/Chris_Rock.jpg')
facec = face_recognition.face_encodings(imgc)[0]
results = face_recognition.compare_faces([facec],faced)
if results == [True]:
    print('ok')
else: print('nah')