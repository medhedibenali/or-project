import sys
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget, QLabel,
)
from src.pl.gui import MainApp as MainWindowPl  # Import the PL GUI main window
from src.plne.gui import MainWindow as MainWindowPlne  # Import the PLNE GUI main window
from src.styles import Styles

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.resize(800, 700)
        self.setStyleSheet("background-color: %s;" % Styles.WINDOW_BACKGROUND_COLOR)

        self.title_label = QLabel("Recherche Opérationnelle")
        self.title_label.setFont(QFont(Styles.FONT_TYPE, 14))
        self.title_label.setStyleSheet("color: %s;" % Styles.BIG_LABEL_COLOR)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFixedHeight(50)
        layout.addWidget(self.title_label)

        self.pl_button = QPushButton("Problème PL")
        self.pl_button.setStyleSheet(
            "font-size: 14px; background-color: %s; color: %s; border: none; padding: 10px 20px; border-radius: 5px;" % (
                Styles.CALCULATE_BUTTON_COLOR, Styles.BUTTON_TEXT_COLOR))
        layout.addWidget(self.pl_button)
        self.pl_button.clicked.connect(self.launch_pl_gui)

        self.plne_button = QPushButton("Problème PLNE")
        self.plne_button.setStyleSheet(
            "font-size: 14px; background-color: %s; color: %s; border: none; padding: 10px 20px; border-radius: 5px;" % (
                Styles.CALCULATE_BUTTON_COLOR, Styles.BUTTON_TEXT_COLOR))
        layout.addWidget(self.plne_button)
        self.plne_button.clicked.connect(self.launch_plne_gui)

    def launch_pl_gui(self):
        self.pl_window = MainWindowPl()
        self.pl_window.show()

    def launch_plne_gui(self):
        self.plne_window = MainWindowPlne()
        self.plne_window.show()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
