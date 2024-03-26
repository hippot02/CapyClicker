import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFrame, QHBoxLayout, \
    QSystemTrayIcon
from PySide6.QtGui import QPixmap, QFont, QIcon
from PySide6.QtCore import Qt
import ctypes

class ClickerWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.click_count, self.points_per_click, self.PRICE_CAPYVIEN, self.PRICE_AMELIORATION_2, self.PRICE_CAPY_FABIEN = self.load_click_data()

        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Capy Clicker')
        self.setGeometry(100, 100, 600, 400)

        # Icone de l'appli
        app_icon = QIcon('asset/images/capy_costard.jpg')
        app.setWindowIcon(app_icon)

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('asset/images/capy_costard.jpg')


        # Layout pour les éléments existants
        existing_layout = QVBoxLayout()

        font = QFont("arial")
        font.setPointSize(16)

        # Affichage des degats
        self.click_damage = QLabel(f'Points par clic {self.points_per_click}')
        self.click_damage.setFont(font)
        existing_layout.addWidget(self.click_damage)

        # Affichage des CapyDollars
        self.click_label = QLabel(f'Nombre de Points: {self.click_count}')
        self.click_label.setAlignment(Qt.AlignCenter)
        self.click_label.setFont(font)
        existing_layout.addWidget(self.click_label)

        # Image
        self.image_label = QLabel(self)
        pixmap = QPixmap('asset/images/capy_gun.jpg')
        self.image_label.setPixmap(pixmap)
        self.image_label.setFixedSize(400, 400)
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
        self.create_amelioration_button("Capyvien Roullin", "Augmente les points par clics de 1", 1, self.PRICE_CAPYVIEN)
        self.create_amelioration_button("Amélioration 2", "Augmente les points par clics de 5", 5, self.PRICE_AMELIORATION_2)
        self.create_amelioration_button("Capy Fabien", "Augmente les points par clics de 10", 10, self.PRICE_CAPY_FABIEN)

        # Layout principal
        main_layout = QHBoxLayout()
        main_layout.addLayout(existing_layout)
        main_layout.addWidget(self.ameliorations_widget)

        self.setLayout(main_layout)

    def create_amelioration_button(self, name, description, points_increase, price):
        def update_and_increase_price():
            nonlocal price
            if self.click_count >= price:
                self.click_count -= price
                self.click_count = round(self.click_count,2)
                self.click_label.setText(f'Nombre de Points: {self.click_count}')
                price += int(price * 0.1)
                button.setText(f"{name}\n{description}\nPrix : {price}")

                self.points_per_click += points_increase
                self.click_damage.setText(f'Dégats par clique  {self.points_per_click}')

                if button.text().startswith("Capyvien"):
                    self.PRICE_CAPYVIEN = price
                elif button.text().startswith("Amélioration 2"):
                    self.PRICE_AMELIORATION_2 = price
                elif button.text().startswith("Capy Fabien"):
                    self.PRICE_CAPY_FABIEN = price

                self.save_click_data()

        button = QPushButton(f"{name}\n{description}\nPrix : {price}")
        button.clicked.connect(update_and_increase_price)
        self.ameliorations_layout.addWidget(button)

        update_and_increase_price()


    def on_click(self, event):
        self.click_count += self.points_per_click
        self.click_label.setText(f'Nombre de Points: {self.click_count}')
        self.save_click_data()

    def load_click_data(self):
        try:
            with open('config.txt', 'r') as f:
                lines = f.readlines()
                if len(lines) >= 5:
                    click_count = int(lines[0].strip())
                    points_per_click = int(lines[1].strip())
                    price_capyvien = int(lines[2].strip())
                    price_amelioration_2 = int(lines[3].strip())
                    price_capy_fabien = int(lines[4].strip())
                    return click_count, points_per_click, price_capyvien, price_amelioration_2, price_capy_fabien
                else:
                    print("Les données dans le fichier config.txt sont incomplètes.")
                    return 0, 1, 10, 50, 100  # Valeurs par défaut
        except FileNotFoundError:
            print("Le fichier config.txt n'existe pas. Création avec les valeurs par défaut.")
            self.save_click_data()
            return 0, 1, 10, 50, 100  # Valeurs par défaut
        except (ValueError, IndexError):
            print("Erreur lors de la lecture des données dans le fichier config.txt.")
            return 0, 1, 10, 50, 100  # Valeurs par défaut

    def save_click_data(self):
        try:
            with open('config.txt', 'w') as f:
                f.write(
                    f"{self.click_count}\n{self.points_per_click}\n{round(self.PRICE_CAPYVIEN, 2)}\n{round(self.PRICE_AMELIORATION_2, 2)}\n{round(self.PRICE_CAPY_FABIEN, 2)}")
        except OSError:
            print("Erreur: Impossible de sauvegarder les données dans le fichier config.txt.")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = ClickerWindow()
    window.show()
    sys.exit(app.exec())
