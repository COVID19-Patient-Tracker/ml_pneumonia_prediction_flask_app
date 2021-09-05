


from flask import Flask,request,abort
from tensorflow import keras
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
model = keras.models.load_model('n_model.h5')

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif','.jpeg']

@app.route("/predict", methods=['POST'])
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
            prediction = model.predict(image)
            # convert image into np array
            # and return prediction
            # convert image in to numpy array
    return str(prediction)

if __name__ == "__main__":
    app.run(port=3000,debug=True)