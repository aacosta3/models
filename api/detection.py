#app.py
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from PIL import Image
import roboflow 
import os

app = Flask(__name__)

#INITIALIZE API ENDPOINT TO MODEL
def model():
    # Robloflow API endpoint and API key
    api_key = "JUAU5HWKwNDfZPnijGBr"

    # Initialize the Roboflow client
    rf = roboflow.Roboflow(api_key)
    
    project = rf.workspace().project("fridge-vision")
    # version of the model
    model = project.version(2).model

    return model

if model() is None:
    print("There is no model.")
else:
    print("Model found")

 
UPLOAD_FOLDER = 'static/uploads/'
PREDICTION_PATH = './static/predictions/prediction.jpg'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    #no file found
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    #no image selected
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename('upload.jpg')
        file = Image.open(file)
        new_size = (640,640)
        file = file.resize(new_size)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Image successfully uploaded')
        # input image
        img = 'static/uploads/' + filename
        # Perform object detection on the input image
        prediction = model().predict(img , confidence=40, overlap=30)
        # output image
        prediction.save(PREDICTION_PATH)
        prediction_data = prediction.json()
        # food detection info
        food_found = []

        for pred in prediction_data['predictions']:
            confidence = pred['confidence'] #gets confidence from a value in the 'predictions' list
            class_name = pred['class'] # gets class name from a value in the 'predictions' list
            food_found.append({'confidence': confidence, 'class_name': class_name})
                
        flash('Prediction successfully done and displayed')
        # RETURN food_found list(the food found and cofidence) and the filename(image prediction name)
        return render_template('index.html', food_found=food_found, filename='prediction.jpg')
    else:
        flash('Allowed image types are - png, jpg, jpeg')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='predictions/' + filename), code=301)
 
if __name__ == "__main__":
    app.run()