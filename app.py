


from flask import Flask,request, make_response, json, Response
from tensorflow import keras
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
app = Flask(__name__)
CORS(app)
model = keras.models.load_model('n_model.h5')
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif','.jpeg']

@app.route("/predict", methods=["POST", "OPTIONS"])
def api_create_order():
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    elif(request.method == "POST"):
        arr = predict()
        return Response(json.dumps(arr),  mimetype='application/json')
    else:
        raise RuntimeError("Weird - don't know how to handle method {}".format(request.method))

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

def predict():
    if request.method == "POST":
        # validate images
        imagefile = request.files['image']
        nameOfFile = secure_filename(imagefile.filename)
        if nameOfFile != '':
            file_ext = os.path.splitext(nameOfFile)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                # abort(400)
                return "Invalid file format."
            image_path = "./images/" + imagefile.filename
            imagefile.save(image_path)
            image = load_img(image_path, target_size=(224,224))
            image = img_to_array(image)
            image = image.reshape(1,image.shape[0],image.shape[1],image.shape[2])
            image = preprocess_input(image)
            prediction = model.predict(image/255)
            # convert image into np array
            # and return prediction
            # convert image in to numpy array
            result = [{"normal":prediction[0][0],"pneumoinia":prediction[0][1]}]
    return result

if __name__ == "__main__":
    app.run(port=3000,debug=True)