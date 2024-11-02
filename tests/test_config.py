import unittest
from app.config import *


class TestPixelightConfig(unittest.TestCase):
    def test_basic_settings(self):
        self.assertEqual(program_name, 'Pixelight')
        self.assertEqual((x_window, y_window, width_window, height_window), (100, 100, 100, 100))
        self.assertEqual(icon_name, '.\\icons\\icon.png')
    
    def test_style(self):
        self.assertEqual(back_color, "background-color: #f5f5dc;")
    
    def test_starting_picture(self):
        self.assertEqual(mode, 'RGB')
        self.assertEqual(size, (1000, 1000))
        self.assertEqual(color, (255, 255, 255))
    
    def test_gui_text(self):
        self.assertEqual(toolbox_title, "Інструменти")
        self.assertEqual(pixelate_text, 'Пікселізація')
        self.assertEqual(color_reduce_text, 'Зменшення кольорів')
        self.assertEqual(reset_text, 'Повернутися на початок')
        self.assertEqual(settings_title, "Налаштування")
        self.assertEqual(brightness_tooltip, "Яскравість")
        self.assertEqual(contrast_tooltip, "Контраст")
        self.assertEqual(blur_tooltip, "Розмиття")
        self.assertEqual(sepia_tooltip, "Сепія")
        self.assertEqual(red_channel_tooltip, "Червоний канал")
        self.assertEqual(color_count_tooltip, "Кількість кольорів")
        self.assertEqual(pixelate_size_tooltip, "Розмір пікселізації")
    
    def test_about_text(self):
        self.assertIn("Про програму Pixelight", about_text)
        self.assertIn("Пікселізація", about_text)
        self.assertIn("Налаштування", about_text)
        self.assertIn("Сепія", about_text)
    
    def test_filter_settings(self):
        self.assertEqual(sepia_colors, ('#704214', '#C0C0C0'))

if __name__ == '__main__':
    unittest.main()
