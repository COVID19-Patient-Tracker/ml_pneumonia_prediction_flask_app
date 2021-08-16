


from flask import Flask,request
from tensorflow import keras
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input

app = Flask(__name__)
model = keras.models.load_model('n_model.h5')

@app.route("/predict", methods=['GET'])
def predict():
    if request.method == "POST":
        # validate images
        f = request.files['image']
        imafe_path = "./images/" + imagefile.filename
        imagefile.save(path)
        image = load_img(image_path, target_size(224,224))
        image = image_to_array(image)
        image = image.reshape(1,image.shape[0],image.shape[1],image.shape[2])
        image = preprocess_input(image)
        prediction = model.predict(image)
        # convert image into np array
        # and return prediction
        # convert image in to numpy array
    return "hello world"

if __name__ == "__main__":
    app.run(port=3000,debug=True)