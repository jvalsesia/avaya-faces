from flask import Flask, send_file
from flask.json import jsonify
from flask.scaffold import F
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from mongoengine import connect, Document, fields
from flask_socketio import SocketIO, emit

import werkzeug
import uuid
import os 
import cv2
import face_recognition
import numpy as np
import base64


app =  Flask(__name__)
CORS(app)
api = Api(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# It will allow below 16MB contents only, you can change it
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
path = os.getcwd()
# file Upload
#ENROLLMENT_FOLDER = os.path.join(path, 'uploads/enrollment')
#RECOGNITION_FOLDER = os.path.join(path, 'uploads/recognition')

# Make directory if "uploads" folder not exists
#if not os.path.isdir(ENROLLMENT_FOLDER):
#    os.mkdir(ENROLLMENT_FOLDER)
#print(ENROLLMENT_FOLDER)
#app.config['ENROLLMENT_FOLDER'] = ENROLLMENT_FOLDER

# Make directory if "uploads" folder not exists
#if not os.path.isdir(RECOGNITION_FOLDER):
#    os.mkdir(RECOGNITION_FOLDER)
#print(RECOGNITION_FOLDER)
#app.config['RECOGNITION_FOLDER'] = RECOGNITION_FOLDER

ALLOWED_EXTENSIONS = set(['.png', '.jpg'])

 # Mongo Database
if os.environ.get('APP_ENV') == 'prod' :
    # Production
    connect(host="mongodb://" + os.environ.get('MONGODB_USERNAME') + ":" + os.environ.get('MONGODB_PASSWORD') + "@" + os.environ.get('MONGODB_HOSTNAME') + ":27017/" + os.environ.get('MONGODB_DATABASE'))
else:
    # Development
    connect(host="mongodb://apiuser:api123!@localhost?27017/facesdb")





#def save_enrollment(user_name, image, file_name, face_encodings):
def save_enrollment(user_name, face_encodings):
     enrollment = UserEnrollment(username=user_name)
     #enrollment.image.replace(image, filename=file_name)
     enrollment.faceencodings = face_encodings
     enrollment.username = user_name
     enrollment.save()


def get_all_username_encodings_zip():
    encodings_list = []
    username_list = []
    for user_enrollment in UserEnrollment.objects:
        encodings_list.append(user_enrollment.faceencodings)
        username_list.append(user_enrollment.username)
    return list(zip(encodings_list, username_list))

class UserEnrollment(Document):
    meta = {"collection":"user_enrollments"}
    username = fields.StringField(required=True)
    #image = fields.ImageField(thumbnail_size=(150,150, False))
    faceencodings = fields.ListField()


class GetEnrollment(Resource):
    def get(self, username):
        user_from_enrollment = UserEnrollment.objects(username=username).first()
        #image_encoded = base64.b64encode(user_from_enrollment.image.read())
        face_encodings = user_from_enrollment.faceencodings
        user_name = user_from_enrollment.username
        print(face_encodings)
        return jsonify({
            #"image": image_encoded.decode('utf-8'), 
            "encodings": face_encodings,
            "username": user_name
            })
        
        

class ProcessEnrollment(Resource):
        def __init__(self):
              # Create a request parser
            parser = reqparse.RequestParser()
            parser.add_argument("image", type=werkzeug.datastructures.FileStorage, location='files', required=True)
            parser.add_argument("username", type=str, help="Username", required=True)

            # Sending more info in the form? simply add additional arguments, with the location being 'form'
            # parser.add_argument("other_arg", type=str, location='form')
            self.req_parser = parser

     
        # This method is called when we send a POST request to this endpoint
        def post(self):
            # The image is retrieved as a file
            image_file = self.req_parser.parse_args(strict=True).get("image", None)
            user_name = self.req_parser.parse_args(strict=True).get("username", None)
            extension = os.path.splitext(image_file.filename)[1]
            print(extension)
            if image_file and extension in ALLOWED_EXTENSIONS:

               
                # Get the byte content using `.read()`
                image = image_file.read()
               
                 # convert to numpy array
                npimg = np.frombuffer(image, np.uint8)
                print(npimg)
                img = cv2.imdecode(npimg, cv2.COLOR_BGR2GRAY)
               
                face_encodings = face_recognition.face_encodings(img)
                print(face_encodings)
                #save_enrollment(user_name, image_file, image_file.filename, face_encodings)
                save_enrollment(user_name, face_encodings)
                #image_path = os.path.join(app.config['ENROLLMENT_FOLDER'], f'{user_name}{extension}')
                #print(image_path)
                #cv2.imwrite(image_path, img)
             
                # Now do something with the image...
                return "You sent an image!"
            else:
                return "No image sent!"

# used to process Base64 images
class ProcessRecognitionBase64(Resource):
    def __init__(self):
        # Create a request parser
        parser = reqparse.RequestParser()
        parser.add_argument("base64image", type=str, help="Base64 encoded image string", required=True, location='json')
        self.req_parser = parser

    # This method is called when we send a POST request to this endpoint
    def post(self):
        user_name = 'Unknown'
        result = {
                    "status: " : "NOT_FOUND",
                    "username" : user_name
                }
            
       	base64image = self.req_parser.parse_args(strict=True).get("base64image", None)
        if base64image:

            # Do something with the base64 string - for example, convert it back to bytes
            byte_content = base64.b64decode(base64image)
        
            im_arr = np.frombuffer(byte_content, dtype=np.uint8)  # im_arr is one-dim Numpy array
            image_to_be_recognized = cv2.imdecode(im_arr, flags=cv2.COLOR_BGR2GRAY)
            face_encodings_to_be_recognized = face_recognition.face_encodings(image_to_be_recognized)
            
            # found_face = []
            # unzip encodings and username lists
            for encodings, username in get_all_username_encodings_zip():
                print(encodings)
                print(username)
                try:
                    found_face = face_recognition.compare_faces(np.array(encodings), np.array(face_encodings_to_be_recognized), 0.6)
            
                    if True in found_face:
                        #first_match_index = found_face.index(True)
                        user_name = username
                        result = {
                            "status: " : "FOUND",
                            "username" : user_name
                        }
                        break
                    else:
                        result = {
                            "status: " : "NOT_FOUND",
                            "username" : user_name
                        }                            
                except:
                    return jsonify({
                "status: " : "ERROR",
                "username": user_name
                })
            # user_uuid = uuid.uuid4()
            # print(user_uuid)

            # save iamge    
            # cv2.imwrite(os.path.join(app.config['RECOGNITION_FOLDER'], f'{user_uuid}.png'), image_to_be_recognized)
            
        else:
       		result = {
                "status: " : "ERROR",
                "username" : user_name
            }
        
        socketio.emit('recognized', result)
        return jsonify(result)




# used to process Raw images
class ProcessRecognitionBlob(Resource):
    def __init__(self):
        # Create a request parser
        parser = reqparse.RequestParser()
        parser.add_argument("image", type=werkzeug.datastructures.FileStorage, location='files', required=True)
        self.req_parser = parser

    # This method is called when we send a POST request to this endpoint
    def post(self):
        user_name = 'Unknown'
        result = {
                    "status: " : "NOT_FOUND",
                    "username" : user_name
                }
        image_file = self.req_parser.parse_args(strict=True).get("image", None)
        if image_file:

            # Get the byte content using `.read()`
            image = image_file.read()
               
        
            im_arr = np.frombuffer(image, dtype=np.uint8)  # im_arr is one-dim Numpy array
            image_to_be_recognized = cv2.imdecode(im_arr, flags=cv2.COLOR_BGR2GRAY)
            face_encodings_to_be_recognized = face_recognition.face_encodings(image_to_be_recognized)

            
            
            # found_face = []
            # unzip encodings and username lists
            for encodings, username in get_all_username_encodings_zip():
                print(encodings)
                print(username)
                try:
                    found_face = face_recognition.compare_faces(np.array(encodings), np.array(face_encodings_to_be_recognized), 0.6)
            
                    if True in found_face:
                        #first_match_index = found_face.index(True)
                        user_name = username
                        result = {
                            "status: " : "FOUND",
                            "username" : user_name
                        }
                        break 
                    else:
                        result = {
                            "status: " : "NOT_FOUND",
                            "username" : user_name
                        }                     
                except:
                    return jsonify({
                "status: " : "ERROR",
                "username": user_name
                })
            # user_uuid = uuid.uuid4()
            # print(user_uuid)

            # save iamge    
            # cv2.imwrite(os.path.join(app.config['RECOGNITION_FOLDER'], f'{user_uuid}.png'), image_to_be_recognized)
           
        else:
       		result = {
                "status: " : "ERROR",
                "username" : user_name
            }
        
        socketio.emit('recognized', result)
        return jsonify(result)



class ListEncodings(Resource):
    # This method is called when we send a POST request to this endpoint
    def get(self):
        username_encodings_zip = get_all_username_encodings_zip()
        return jsonify(username_encodings_zip)
        



api.add_resource(GetEnrollment, '/getenroll/<string:username>')
api.add_resource(ProcessEnrollment, '/enroll')
api.add_resource(ProcessRecognitionBase64, '/recognitionbase64')
api.add_resource(ProcessRecognitionBlob, '/recognitionblob')
api.add_resource(ListEncodings, '/encodings')


if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), host='0.0.0.0', port=5500, debug=False, threaded=True)
    socketio.run(app)
