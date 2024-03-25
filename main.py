import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class ClickerWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.click_count = 0

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Clicker')
        self.setGeometry(100, 100, 300, 200)

        self.click_label = QLabel('Nombre de Points: 0', self)
        self.click_label.setAlignment(Qt.AlignCenter)

        self.image_label = QLabel(self)
        pixmap = QPixmap('classique.jpg')
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.mousePressEvent = self.on_click

        layout = QVBoxLayout()
        layout.addWidget(self.click_label)
        layout.addWidget(self.image_label)

        self.setLayout(layout)

    def on_click(self, event):
        self.click_count += 1
        self.click_label.setText(f'Nombre de Points: {self.click_count}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ClickerWindow()
    window.show()
    sys.exit(app.exec())
