import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from src.pl.gui import MainApp as MainWindowPl  # Import the PL GUI main window
from src.plne.gui import MainWindow as MainWindowPlne  # Import the PLNE GUI main window


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.pl_button = QPushButton("Launch PL GUI")
        layout.addWidget(self.pl_button)
        self.pl_button.clicked.connect(self.launch_pl_gui)

        self.plne_button = QPushButton("Launch PLNE GUI")
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
