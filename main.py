import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFrame, QHBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class ClickerWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.click_count, self.points_per_click = self.load_click_data()

        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Capy Clicker')
        self.setGeometry(100, 100, 600, 400)

        # Layout pour les éléments existants
        existing_layout = QVBoxLayout()

        self.click_label = QLabel(f'Nombre de Points: {self.click_count}')
        self.click_label.setAlignment(Qt.AlignCenter)
        existing_layout.addWidget(self.click_label)

        self.image_label = QLabel(self)
        pixmap = QPixmap('classique.jpg')
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.mousePressEvent = self.on_click
        existing_layout.addWidget(self.image_label)

        # Widget pour les améliorations
        self.ameliorations_widget = QFrame(self)
        self.ameliorations_widget.setFrameShape(QFrame.Box)
        self.ameliorations_widget.setFrameShadow(QFrame.Sunken)

        # Layout pour les améliorations
        self.ameliorations_layout = QVBoxLayout(self.ameliorations_widget)
        self.ameliorations_layout.setAlignment(Qt.AlignTop)

        # Boutons pour les améliorations
        self.create_amelioration_button("Capyvien Roullin", "Augmente les points par clics de 1", 1)
        self.create_amelioration_button("Amélioration 2", "Augmente les points par clics de 5", 5)
        self.create_amelioration_button("Capy Fabien", "Augmente les points par clics de 10", 10)

        # Layout principal
        main_layout = QHBoxLayout()
        main_layout.addLayout(existing_layout)
        main_layout.addWidget(self.ameliorations_widget)

        self.setLayout(main_layout)

    def create_amelioration_button(self, name, description, points_increase):
        button = QPushButton(f"{name}\n{description}")
        button.clicked.connect(lambda: self.update_points_per_click(points_increase))
        self.ameliorations_layout.addWidget(button)

    def update_points_per_click(self, points_increase):
        self.points_per_click += points_increase
        self.save_click_data()

    def on_click(self, event):
        self.click_count += self.points_per_click
        self.click_label.setText(f'Nombre de Points: {self.click_count}')
        self.save_click_data()

    def load_click_data(self):
        try:
            with open('config.txt', 'r') as f:
                lines = f.readlines()
                if len(lines) >= 2:
                    click_count = int(lines[0].strip())
                    points_per_click = int(lines[1].strip())
                    return click_count, points_per_click
                else:
                    print("Les données dans le fichier config.txt sont incomplètes.")
                    return 0, 1  # Valeurs par défaut
        except FileNotFoundError:
            print("Le fichier config.txt n'existe pas. Création avec les valeurs par défaut.")
            self.save_click_data()
            return 0, 1  # Valeurs par défaut
        except (ValueError, IndexError):
            print("Erreur lors de la lecture des données dans le fichier config.txt.")
            return 0, 1  # Valeurs par défaut

    def save_click_data(self):
        try:
            with open('config.txt', 'w') as f:
                f.write(f"{self.click_count}\n{self.points_per_click}")
        except OSError:
            print("Erreur: Impossible de sauvegarder les données dans le fichier config.txt.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ClickerWindow()
    window.show()
    sys.exit(app.exec())
