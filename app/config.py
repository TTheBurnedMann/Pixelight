import sys
from collections import deque
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox, QWidget, QPushButton, QSlider, QGroupBox,QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PIL import Image, ImageEnhance, ImageFilter, ImageOps


# Basic Settings
program_name = 'Pixelight'
x_window, y_window, width_window, height_window = 100, 100, 100, 100
icon_name = '.\icons\icon.png'

# Style
back_color = "background-color: #f5f5dc;"

# Starting picture
mode = 'RGB'
size = (1000, 1000)
color = (255, 255, 255)

#GUI names for elements

toolbox_title = "Інструменти"
pixelate_text = 'Пікселізація'
color_reduce_text = 'Зменшення кольорів'
reset_text = 'Повернутися на початок'
settings_title = "Налаштування"
brightness_tooltip = "Яскравість"
contrast_tooltip = "Контраст"
blur_tooltip = "Розмиття"
sepia_tooltip = "Сепія"
red_channel_tooltip = "Червоний канал"
color_count_tooltip = "Кількість кольорів"
pixelate_size_tooltip = "Розмір пікселізації"

# Text

about_text = '''Про програму Pixelight
            Pixelight — це потужний редактор зображень, створений для спрощення процесу редагування та налаштування зображень. Завдяки інтуїтивно зрозумілому інтерфейсу, ви зможете легко застосовувати різноманітні ефекти та налаштування до ваших фотографій.

            Основні можливості:
            Пікселізація: Зменшення розміру пікселів для створення художніх ефектів.
            Зменшення кольорів: Адаптація палітри зображення до заданої кількості кольорів.
            Регулювання яскравості: Налаштування рівня яскравості зображення для досягнення бажаного вигляду.
            Регулювання контрасту: Підвищення або зменшення контрастності зображення.
            Застосування розмиття: Додавання ефекту розмиття для створення м'якого вигляду.
            Сепія: Додавання теплого сепійного відтінку для класичного вигляду.
            Керування кольоровими каналами: Налаштування рівня червоного каналу для корекції кольору.
            Інтерфейс:
            Програма має три основні області:

            Інструменти: Різноманітні кнопки для швидкого доступу до функцій редагування.
            Зображення: Основна область для перегляду та редагування зображення.
            Налаштування: Слайдери для регулювання параметрів зображення.
            Як користуватися:
            Відкрийте зображення за допомогою меню Файл.
            Використовуйте інструменти та слайдери, щоб налаштувати зображення на свій смак.
            Зберігайте відредаговане зображення через меню Файл.
            Pixelight — це ідеальний інструмент для тих, хто хоче покращити свої фотографії без зайвих зусиль.'''


# Filters Settings
sepia_colors = '#704214', '#C0C0C0'