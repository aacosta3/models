import os
import sys
import unittest
from PIL import Image
from unittest.mock import patch, Mock, mock_open

# Get the absolute path of the directory containing the test file
test_dir = os.path.dirname(os.path.abspath(__file__))

# Get the absolute path of the project's root directory (assuming the test file is in a subdirectory)
project_root = os.path.abspath(os.path.join(test_dir, ".."))

# Add the project root to sys.path so Python can find modules in your project
sys.path.append(project_root)

from models.food_detection import FoodDetect

class TestFoodDetect(unittest.TestCase):
    def setUp(self):
        self.food_detector = FoodDetect()

    def tearDown(self):
        pass

    def test_allowed_file(self):
        # Test allowed file extensions
        self.assertTrue(self.food_detector.allowed_file("image.jpg"))
        self.assertTrue(self.food_detector.allowed_file("image.png"))
        self.assertTrue(self.food_detector.allowed_file("image.jpeg"))

        # Test disallowed file extensions
        self.assertFalse(self.food_detector.allowed_file("image.txt"))
        self.assertFalse(self.food_detector.allowed_file("image.gif"))

    def test_process_image(self):
        # Test image resizing
        # You may need to provide actual images for testing
        # Ensure the expected image size matches the dimensions specified in the process_image method
        test_image = Image.open("test/testimg.jpg")
        processed_image = self.food_detector.process_image(test_image)
        expected_size = (640, 640)
        self.assertEqual(processed_image.size, expected_size)

    @patch('os.makedirs')
    @patch('os.path.exists', return_value=False)
    @patch('PIL.Image.Image.save')
    def test_upload_image(self, mock_save, mock_path_exists, mock_makedirs):
        test_image = Image.open("test/testimg.jpg")
        upload_path = "./static/uploads/"
        self.food_detector.upload_image(test_image, upload_path)
        
        # Verify if the image would have been saved to the right path
        expected_save_path = os.path.join(upload_path, 'upload.jpg')
        mock_save.assert_called_with(expected_save_path)

    @patch('os.makedirs')
    @patch('os.path.exists', return_value=False)
    def test_predict_image(self, mock_path_exists, mock_makedirs):
        mock_prediction = Mock()
        mock_prediction.json.return_value = [{'confidence': 0.85, 'class_name': 'apple'}]
        
        with patch.object(self.food_detector.model, 'predict', return_value=mock_prediction):
            prediction_path = './static/predictions/'
            self.food_detector.predict_image(prediction_path)

            # Check if the mock prediction's save method was called with the expected path
            expected_save_path = os.path.join(prediction_path, 'prediction.jpg')
            mock_prediction.save.assert_called_with(expected_save_path)

    def test_get_results(self):
        # Mocked prediction data for the FoodDetect class
        self.food_detector.prediction_data = {
            'predictions': [
                {'confidence': 0.85, 'class': 'apple'},
                {'confidence': 0.75, 'class': 'banana'}
            ]
        }

        results = self.food_detector.get_results()

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['confidence'], 0.85)
        self.assertEqual(results[0]['class'], 'apple')
        self.assertEqual(results[1]['confidence'], 0.75)
        self.assertEqual(results[1]['class'], 'banana')

    def test_clear_images(self):
        # First, we'll manually create dummy images to simulate the real environment.
        open('./static/uploads/upload.jpg', 'a').close()  # Create a dummy upload image.
        open('./static/predictions/prediction.jpg', 'a').close()  # Create a dummy prediction image.

        # Now, use the clear_images method to try and delete them.
        self.food_detector.clear_images()

        # Assert that the images have been deleted.
        self.assertFalse(os.path.exists('./static/uploads/upload.jpg'))
        self.assertFalse(os.path.exists('./static/predictions/prediction.jpg'))
        
    def test_check_model(self):
        model = self.food_detector.check_model()

        # Assert that the model is not None (i.e., a model is returned)
        self.assertIsNotNone(model)

        # If you know specific attributes or methods the model should have, you can assert their presence.
        # For example, if the model should have a 'predict' method:
        self.assertTrue(hasattr(model, 'predict'))

if __name__ == "__main__":
    unittest.main()
