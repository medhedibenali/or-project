from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLineEdit, QLabel, QPushButton, QWidget


class BaseWidget(QWidget):
    FONT_TYPE = "Segoe UI"
    INPUT_TEXT_COLOR = "#fbfaee"
    LABEL_COLOR = "white"
    LIGHT_BG_COLOR = "#fbfaee"
    BUTTON_TEXT_COLOR = "white"
    WINDOW_BACKGROUND_COLOR = "#242424"

    def __init__(self):
        super().__init__()

    def apply_common_styles(self, widget, font_size):
        if isinstance(widget, QLineEdit):
            widget.setStyleSheet(f"color: {self.INPUT_TEXT_COLOR}; \
                                  border-radius: 5px; \
                                  border: none; \
                                  background-color: {self.LIGHT_BG_COLOR};")
        elif isinstance(widget, QLabel):
            widget.setStyleSheet(f"color: {self.LABEL_COLOR};")
        elif isinstance(widget, QPushButton):
            widget.setStyleSheet(f"font-size: {font_size}px; \
                                  background-color: {self.LIGHT_BG_COLOR}; \
                                  color: {self.BUTTON_TEXT_COLOR}; \
                                  border: none; \
                                  padding: 5px 10px; \
                                  border-radius: 5px;")
        widget.setFont(QFont(self.FONT_TYPE, font_size))
