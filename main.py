import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QMessageBox)
from analyze_image import analyze_image


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Object Detector")
        self.setGeometry(300, 300, 300, 200)

        layout = QVBoxLayout()

        self.btn_upload = QPushButton("Загрузить изображение")
        self.btn_upload.clicked.connect(self.load_image)

        self.btn_exit = QPushButton("Выход")
        self.btn_exit.clicked.connect(self.close)

        layout.addWidget(self.btn_upload)
        layout.addWidget(self.btn_exit)

        self.setLayout(layout)

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.tiff)"
        )

        if file_path:
            try:
                analyze_image(file_path)

                QMessageBox.information(
                    self,
                    "Успех",
                    "Изображение успешно обработано!"
                )

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Ошибка",
                    str(e)
                )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
