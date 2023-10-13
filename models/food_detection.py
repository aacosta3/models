from PIL import Image
import roboflow 
import os


#INITIALIZE API ENDPOINT TO MODEL


class FoodDetect:

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


    def __init__(self):
        self.UPLOAD_PATH = ''

        self.prediction_data = []
        # Roboflow API endpoint and API key
        self.api_key = "JUAU5HWKwNDfZPnijGBr"

        # Initialize the Roboflow client
        self.rf = roboflow.Roboflow(self.api_key)
    
        # Project and model initialization
        self.project = self.rf.workspace().project("fridge-vision")
        self.model = self.project.version(8).model


    # Restriction to what file images to allow
    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    # Resize image for best food detection performance
    def process_image(self, image):
        #image = Image.open(image)
        dimensions = (640, 640)
        return image.resize(dimensions)

    # Image is saved in the path specified
    def upload_image(self, file, path):
        if file and self.allowed_file(file.filename):
            print(file.filename + " is correct file image format")
            if not os.path.exists(path):
                os.makedirs(path)
                
            image = self.process_image(file)
            image.save(os.path.join(path, "upload.jpg"))
            self.UPLOAD_PATH = path + 'upload.jpg'
            print(file.filename + " was saved correctly to " + path)

     # Here the model predicts what food is in the image
    def predict_image(self, path):
        image = self.UPLOAD_PATH
        prediction = self.model.predict(image , confidence=40, overlap=30)
        self.prediction_data = prediction.json()
        if not os.path.exists(path):
                os.makedirs(path)

        prediction.save(os.path.join(path, "prediction.jpg"))
        print('Prediction was complete and saved in ' + path)

    def get_results(self):
        
        food_found = []
        for pred in self.prediction_data['predictions']:
            confidence = pred['confidence'] #gets confidence from a value in the 'predictions' list
            class_name = pred['class'] # gets class name from a value in the 'predictions' list
            food_found.append({'confidence': confidence, 'class': class_name})
        return food_found    

    def clear_images(self):
        """Delete the uploaded and predicted images."""
        upload_image_path = os.path.join('./static/uploads/', 'upload.jpg')
        prediction_image_path = os.path.join('./static/predictions/', 'prediction.jpg')

        # Check and remove uploaded image
        if os.path.exists(upload_image_path):
            os.remove(upload_image_path)
            print('Uploaded image removed successfully.')

        # Check and remove predicted image
        if os.path.exists(prediction_image_path):
            os.remove(prediction_image_path)
            print('Predicted image removed successfully.')
            
    def check_model(self):
        return self.model
    
    
        
