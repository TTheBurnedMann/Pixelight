
from config import *

class ImageEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        #основні настройки
        self.setWindowTitle(program_name)
        self.setGeometry(x_window, y_window, width_window, height_window)
        self.setWindowIcon(QIcon(icon_name))
        
        # Бежевий стиль
        self.setStyleSheet(back_color) 

        # Центральна область для зображення
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        # Ініціалізація з порожнім зображенням
        self.original_image = Image.new(mode, size, color)
        self.image = self.original_image.copy()
        self.image1 = self.original_image.copy()
        self.history = deque(maxlen=5)  # Історія змін (5 кроків)
        self.history.append(self.image.copy())  # Додаємо оригінальне зображення в історію
        self.update_image_label()

        # Додаємо QScrollArea для прокрутки зображення
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.image_label)

        self.scale_factor = 1.0

        # Головний контейнер для зображення
        self.image_container = QWidget(self)
        self.image_layout = QVBoxLayout()
        self.image_layout.addWidget(self.scroll_area)
        self.image_container.setLayout(self.image_layout)

        # Лівий бокс з кнопками інструментів
        left_box = QGroupBox("Інструменти")
        left_layout = QVBoxLayout()

        self.pixelate_button = QPushButton('Пікселізація')
        self.pixelate_button.clicked.connect(self.pixelate_image)
        self.color_reduce_button = QPushButton('Зменшення кольорів')
        self.color_reduce_button.clicked.connect(self.reduce_colors)
        self.reset_button = QPushButton('Повернутися на початок')
        self.reset_button.clicked.connect(self.reset_image)

        left_layout.addWidget(self.pixelate_button)
        left_layout.addWidget(self.color_reduce_button)
        left_layout.addWidget(self.reset_button)

        left_box.setLayout(left_layout)

        # Правий бокс з налаштуваннями
        right_box = QGroupBox("Налаштування")
        right_layout = QVBoxLayout()

        # Налаштування зображення з повзунками
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(0, 100)
        self.brightness_slider.setValue(50)
        self.brightness_slider.setToolTip("Яскравість")
        self.brightness_slider.valueChanged.connect(self.adjust_image)

        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(0, 100)
        self.contrast_slider.setValue(50)
        self.contrast_slider.setToolTip("Контраст")
        self.contrast_slider.valueChanged.connect(self.adjust_image)

        self.blur_slider = QSlider(Qt.Horizontal)
        self.blur_slider.setRange(0, 10)
        self.blur_slider.setValue(0)
        self.blur_slider.setToolTip("Розмиття")
        self.blur_slider.valueChanged.connect(self.adjust_image)

        self.sepia_slider = QSlider(Qt.Horizontal)
        self.sepia_slider.setRange(0, 100)
        self.sepia_slider.setValue(0)
        self.sepia_slider.setToolTip("Сепія")
        self.sepia_slider.valueChanged.connect(self.adjust_image)

        self.red_channel_slider = QSlider(Qt.Horizontal)
        self.red_channel_slider.setRange(0, 100)
        self.red_channel_slider.setValue(100)
        self.red_channel_slider.setToolTip("Червоний канал")
        self.red_channel_slider.valueChanged.connect(self.adjust_image)

        # Слайдери для зменшення кольорів і піксалізації
        self.color_count_slider = QSlider(Qt.Horizontal)
        self.color_count_slider.setRange(2, 256)  # Від 2 до 256 кольорів
        self.color_count_slider.setValue(16)
        self.color_count_slider.setToolTip("Кількість кольорів")

        self.pixelate_size_slider = QSlider(Qt.Horizontal)
        self.pixelate_size_slider.setRange(1, 100)  # Від 1 до 50 пікселів
        self.pixelate_size_slider.setValue(1)
        self.pixelate_size_slider.setToolTip("Розмір пікселізації")

        right_layout.addWidget(QLabel("Яскравість"))
        right_layout.addWidget(self.brightness_slider)
        right_layout.addWidget(QLabel("Контраст"))
        right_layout.addWidget(self.contrast_slider)
        right_layout.addWidget(QLabel("Розмиття"))
        right_layout.addWidget(self.blur_slider)
        right_layout.addWidget(QLabel("Сепія"))
        right_layout.addWidget(self.sepia_slider)
        right_layout.addWidget(QLabel("Червоний канал"))
        right_layout.addWidget(self.red_channel_slider)
        right_layout.addWidget(QLabel("Кількість кольорів"))
        right_layout.addWidget(self.color_count_slider)
        right_layout.addWidget(QLabel("Розмір пікселізації"))
        right_layout.addWidget(self.pixelate_size_slider)

        right_box.setLayout(right_layout)

        # Меню
        menu = self.menuBar()
        file_menu = menu.addMenu('File')

        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_image)
        file_menu.addAction(save_action)

        save_as_action = QAction('Save As', self)
        save_as_action.triggered.connect(self.save_as_image)
        file_menu.addAction(save_as_action)

        about_menu = menu.addMenu('About')
        about_action = QAction('Info', self)
        about_action.triggered.connect(self.show_about)
        about_menu.addAction(about_action)

        # Головний макет
        main_layout = QHBoxLayout()
        main_layout.addWidget(left_box)
        main_layout.addWidget(self.image_container)
        main_layout.addWidget(right_box)

        container = QWidget()
        container.setLayout(main_layout)

        self.setCentralWidget(container)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            self.original_image = Image.open(file_name).convert('RGB')  # Конвертуємо зображення в RGB
            self.image = self.original_image.copy()
            self.update_image_label()

    def save_image(self):
        if self.image:
            self.image.save("output.png")

    def save_as_image(self):
        if self.image:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Image As", "", "PNG Files (*.png);;JPEG Files (*.jpg)")
            if file_name:
                self.image.save(file_name)

    def update_image_label(self):
        
        qimage = QImage(self.image.tobytes(), self.image.width, self.image.height, self.image.width * 3, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap)
        

    def show_about(self):
        # Використання QMessageBox для відображення повідомлення
        about_msg = QMessageBox(self)
        about_msg.setWindowTitle("Про програму")
        about_msg.setText('''Про програму Pixelight
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
            Pixelight — це ідеальний інструмент для тих, хто хоче покращити свої фотографії без зайвих зусиль.''')
        about_msg.setIcon(QMessageBox.Information)
        about_msg.setStandardButtons(QMessageBox.Ok)
        about_msg.exec_()  # Викликає модальне вікно

    def adjust_image(self):
 
            pixelate_size = self.pixelate_size_slider.value()
            self.image = self.original_image.copy()  # Повертаємося до початкового зображення
            self.image = self.image.resize(
                (self.image.width // pixelate_size, self.image.height // pixelate_size),
                Image.NEAREST
            )
            self.image = self.image.resize(
                (self.image.width * pixelate_size, self.image.height * pixelate_size),
                Image.NEAREST
            )

            color_count = self.color_count_slider.value()
            self.image = self.image.convert('P', palette=Image.ADAPTIVE, colors=color_count).convert('RGB')
            
            # Застосовуємо яскравість
            brightness = ImageEnhance.Brightness(self.image)
            self.image = brightness.enhance(self.brightness_slider.value() / 50)
            # Застосовуємо контраст
            contrast = ImageEnhance.Contrast(self.image)
            self.image = contrast.enhance(self.contrast_slider.value() / 50)
            # Застосовуємо розмиття
            blur_value = self.blur_slider.value()
            self.image = self.image.filter(ImageFilter.GaussianBlur(radius=blur_value))
            # Застосовуємо сепію
            sepia_strength = self.sepia_slider.value()
            sepia_image = ImageOps.colorize(self.image.convert('L'), '#704214', '#C0C0C0')  # Застосування сепії
            self.image = Image.blend(self.image, sepia_image, sepia_strength / 100.0)
            # Застосовуємо червоний канал
            red_channel_multiplier = self.red_channel_slider.value() / 100
            r, g, b = self.image.split()
            r = r.point(lambda i: i * red_channel_multiplier)
            self.image = Image.merge(mode, (r, g, b))
            # Оновлюємо зображення
            self.update_image_label()

    def pixelate_image(self):
        self.adjust_image()
        
    def reduce_colors(self):
        self.adjust_image()

    def reset_image(self):
        """Повернення до оригінального зображення"""
        self.image = self.original_image.copy()
        self.update_image_label()

    def wheelEvent(self, event):
        """Обробка події прокрутки миші для масштабування зображення."""
        # Визначаємо напрямок прокрутки
        if event.angleDelta().y() > 0:  # Прокрутка вгору
            self.scale_factor *= 1.1  # Збільшення масштабу
        else:  # Прокрутка вниз
            self.scale_factor /= 1.1  # Зменшення масштабу

        # Застосовуємо масштаб до зображення
        self.update_scaled_image()

    def update_scaled_image(self):
        """Оновлює зображення відповідно до поточного масштабу."""
        # Масштабування зображення
        new_size = (int(self.original_image.width * self.scale_factor), int(self.original_image.height * self.scale_factor))
        scaled_image = self.image.resize(new_size, Image.LANCZOS)  # Використання LANCZOS для покращення якості

        # Оновлюємо зображення
        self.image = scaled_image
        self.update_image_label()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = ImageEditor()
    editor.show()
    sys.exit(app.exec_())
