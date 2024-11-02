from PyQt5.QtWidgets import QFileDialog
from PIL import Image


class ImageFileOperations:
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
