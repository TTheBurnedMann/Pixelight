import unittest
import os
import sys

sys.path.append(os.path.abspath("D:/pythonp/lab3/app"))
from app.main import *

class TestImageEditor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Створення екземпляра QApplication перед усіма тестами."""
        cls.app = QApplication([])

    @classmethod
    def tearDownClass(cls):
        """Закриття QApplication після всіх тестів."""
        cls.app.quit()

    def setUp(self):
        """Створення екземпляра ImageEditor перед кожним тестом."""
        self.image_editor = ImageEditor()

    def test_initialization(self):
        """Перевірка, чи ініціалізація виконується правильно."""
        self.assertEqual(self.image_editor.windowTitle(), "Pixelight")  
        self.assertIsNotNone(self.image_editor.original_image) 

    def test_buttons_exist(self):
        """Перевірка, чи всі кнопки присутні в інтерфейсі."""
        self.assertIsNotNone(self.image_editor.pixelate_button)
        self.assertIsNotNone(self.image_editor.color_reduce_button)
        self.assertIsNotNone(self.image_editor.reset_button)

    def test_menu_actions(self):
        """Перевірка, чи дії меню працюють без помилок."""
        self.image_editor.open_file() 
        self.image_editor.save_image()
        self.image_editor.save_as_image()

if __name__ == "__main__":
    unittest.main()
