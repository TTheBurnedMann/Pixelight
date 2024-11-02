


from config import *
from file_management import ImageFileOperations
from image_enhance import ImageProcessor


class ImageEditor(QMainWindow, ImageFileOperations, ImageProcessor):
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
        left_box = QGroupBox(toolbox_title)
        left_layout = QVBoxLayout()

        self.pixelate_button = QPushButton(pixelate_text)
        self.pixelate_button.clicked.connect(self.pixelate_image)
        self.color_reduce_button = QPushButton(color_reduce_text)
        self.color_reduce_button.clicked.connect(self.reduce_colors)
        self.reset_button = QPushButton(reset_text)
        self.reset_button.clicked.connect(self.reset_image)

        left_layout.addWidget(self.pixelate_button)
        left_layout.addWidget(self.color_reduce_button)
        left_layout.addWidget(self.reset_button)

        left_box.setLayout(left_layout)

        # Правий бокс з налаштуваннями
        right_box = QGroupBox(settings_title)
        right_layout = QVBoxLayout()

        # Налаштування зображення з повзунками
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(0, 100)
        self.brightness_slider.setValue(50)
        self.brightness_slider.setToolTip(brightness_tooltip)
        self.brightness_slider.valueChanged.connect(self.adjust_image)

        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(0, 100)
        self.contrast_slider.setValue(50)
        self.contrast_slider.setToolTip(contrast_tooltip)
        self.contrast_slider.valueChanged.connect(self.adjust_image)

        self.blur_slider = QSlider(Qt.Horizontal)
        self.blur_slider.setRange(0, 10)
        self.blur_slider.setValue(0)
        self.blur_slider.setToolTip(blur_tooltip)
        self.blur_slider.valueChanged.connect(self.adjust_image)

        self.sepia_slider = QSlider(Qt.Horizontal)
        self.sepia_slider.setRange(0, 100)
        self.sepia_slider.setValue(0)
        self.sepia_slider.setToolTip(sepia_tooltip)
        self.sepia_slider.valueChanged.connect(self.adjust_image)

        self.red_channel_slider = QSlider(Qt.Horizontal)
        self.red_channel_slider.setRange(0, 100)
        self.red_channel_slider.setValue(100)
        self.red_channel_slider.setToolTip(red_channel_tooltip)
        self.red_channel_slider.valueChanged.connect(self.adjust_image)

        # Слайдери для зменшення кольорів і піксалізації
        self.color_count_slider = QSlider(Qt.Horizontal)
        self.color_count_slider.setRange(2, 256)  # Від 2 до 256 кольорів
        self.color_count_slider.setValue(256)
        self.color_count_slider.setToolTip(color_count_tooltip)

        self.pixelate_size_slider = QSlider(Qt.Horizontal)
        self.pixelate_size_slider.setRange(1, 100)  # Від 1 до 50 пікселів
        self.pixelate_size_slider.setValue(1)
        self.pixelate_size_slider.setToolTip(pixelate_size_tooltip)

        right_layout.addWidget(QLabel(brightness_tooltip))
        right_layout.addWidget(self.brightness_slider)
        right_layout.addWidget(QLabel(contrast_tooltip))
        right_layout.addWidget(self.contrast_slider)
        right_layout.addWidget(QLabel(blur_tooltip))
        right_layout.addWidget(self.blur_slider)
        right_layout.addWidget(QLabel(sepia_tooltip))
        right_layout.addWidget(self.sepia_slider)
        right_layout.addWidget(QLabel(red_channel_tooltip))
        right_layout.addWidget(self.red_channel_slider)
        right_layout.addWidget(QLabel(color_count_tooltip))
        right_layout.addWidget(self.color_count_slider)
        right_layout.addWidget(QLabel(pixelate_size_tooltip))
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

    def show_about(self):
        # Використання QMessageBox для відображення повідомлення
        about_msg = QMessageBox(self)
        about_msg.setWindowTitle("Про програму")
        about_msg.setText(about_text)
        about_msg.setIcon(QMessageBox.Information)
        about_msg.setStandardButtons(QMessageBox.Ok)
        about_msg.exec_()  # Викликає модальне вікно

    def wheelEvent(self, event):
        """Обробка події прокрутки миші для масштабування зображення."""
        # Визначаємо напрямок прокрутки
        if event.angleDelta().y() > 0:  # Прокрутка вгору
            self.scale_factor *= 1.1 
        else:  # Прокрутка вниз
            self.scale_factor /= 1.1 

        # Застосовуємо масштаб до зображення
        self.update_scaled_image()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = ImageEditor()
    editor.show()
    sys.exit(app.exec_())
