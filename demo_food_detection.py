from models.food_detection import FoodDetect
from PIL import Image
# Create an instance of the FoodDetect class
food_detector = FoodDetect()

if food_detector.check_model is None:
    print("There is no model.")
else:
    print("Model found")

image = Image.open("test/testimg.jpg")

UPLOADS_FOLDER = './static/uploads/'
PREDICTIONS_FOLDER = './static/predictions/'

food_detector.upload_image(image, UPLOADS_FOLDER)

food_detector.predict_image(PREDICTIONS_FOLDER)

#food_detector.clear_images()

for food in food_detector.get_results():
    print('Confidence: ',food['confidence'], ' class name: ',  food['class'])
    