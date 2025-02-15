from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton
)
from PySide6.QtGui import QFont

class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title Label
        title_label = QLabel("My Project")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        layout.addWidget(title_label)

        # Description Label
        description_label = QLabel(
            "This project demonstrates a simple PySide6 GUI application.\n"
            "Click the button below to go to the form view."
        )
        description_label.setWordWrap(True)
        layout.addWidget(description_label)

        # Button to switch to the Form view
        self.go_to_form_btn = QPushButton("Go to Form")
        layout.addWidget(self.go_to_form_btn)

        layout.addStretch()  # Pushes the content to the top
        self.setLayout(layout)
