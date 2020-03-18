from flask import Flask, request
import cv2 
import os 
import platform
import face_recognition
import cv2
from datetime import datetime, timedelta
import numpy as np
import pickle
import pathlib
import face_utils
from flask_cors import CORS
import base64

with open('known_faces_data.dat', 'rb') as f:
    known_face_encodings, known_face_metadata = pickle.load(f)

app = Flask(__name__)
CORS(app)
@app.route("/api/checkimage",methods =["POST"])
def checkimage():
    if request.method =="POST":
        try:
            f = 1
            filestr = request.files['File'].read()
            # print(filestr)
            npimg = np.fromstring(filestr, np.uint8) #convert string data to numpy array
            frame = cv2.imdecode(npimg,1) # convert numpy array to image
            face_locations, face_encodings = face_utils.detect_face(frame, f)
            
            if(len(face_locations) != 0):
                for (ftop, fright, fbottom, fleft), face_encoding in zip(face_locations, face_encodings):
                    # look for face and get name
                    uname, distance = face_utils.lookup_known_face(face_encoding, known_face_encodings, known_face_metadata) 

                    # display
                    ftop *= f
                    fright *= f
                    fbottom *= f
                    fleft *= f
                    cv2.rectangle(frame, (fleft, ftop), (fright, fbottom), (0,0,255), 2)
                    bbox = (fleft, ftop, fright, fbottom)
                    centroid = ((bbox[0]+bbox[2])//2, (bbox[1]+bbox[3])//2)
                    cv2.circle(frame, centroid, 4, (255,0,0), -1)
                    cv2.putText(frame, uname, (bbox[0] + 6, bbox[3] - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
                    cv2.putText(frame, str(distance), (0, 25), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
                checkFace = True
            else:
                checkFace = False

            print("write")
            cv2.imwrite('./result.jpeg', frame)
    
            with open('./result.jpeg','rb') as f:
                io_img = f.read()
            my_string = base64.b64encode(io_img)
            str_b64   = my_string.decode('utf-8')
            url_b64   = "data:image/jpeg;base64,{}".format(str_b64)
            print("======")

            if checkFace:
                return {"Message": "Sucess","DATA":str(uname), "Image": url_b64}, 200
            if not(checkFace):
                return {"Message": "Sucess","DATA":"No Face", "Image": url_b64}, 200
        except Exception as e:
            print(e)
            return {"Message": "Failed"}, 500


if __name__ == '__main__':
    app.run(host ='0.0.0.0',port=8000)
