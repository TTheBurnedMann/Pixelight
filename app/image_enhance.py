from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from PyQt5.QtGui import QImage, QPixmap
from config import *  # Імпорт усіх параметрів з config

class ImageProcessor:
    def update_image_label(self):
        
        qimage = QImage(self.image.tobytes(), self.image.width, self.image.height, self.image.width * 3, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap)
        
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
            self.image = self.image.convert('P', palette=Image.ADAPTIVE, colors=color_count).convert(mode)
            
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
            sepia_image = ImageOps.colorize(self.image.convert('L'), sepia_colors[0], sepia_colors[1])  # Застосування сепії
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

    def update_scaled_image(self):
        """Оновлює зображення відповідно до поточного масштабу."""
        # Масштабування зображення
        new_size = (int(self.original_image.width * self.scale_factor), int(self.original_image.height * self.scale_factor))
        scaled_image = self.image.resize(new_size, Image.LANCZOS)  # Використання LANCZOS для покращення якості

        # Оновлюємо зображення
        self.image = scaled_image
        self.update_image_label()
