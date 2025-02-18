"""
HomePage Module

This module defines the `HomePage` class, which serves as the main landing page 
for a PySide6 GUI application. It displays a title, a brief description, and a 
button to navigate to the form page.
"""


from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton
)
from PySide6.QtGui import QFont
from gui.form_page import FormPage


class HomePage(QWidget):
    """
    A QWidget subclass that represents the home page of the application.

    The home page displays:
    - A title label.
    - A description label with an overview of the application.
    - A button to navigate to the form page.

    Args:
        parent (QWidget, optional): The parent widget. Defaults to None.
    """

    def __init__(self, parent, stack):
        """
        Initializes the HomePage with a title, description, and navigation button.

        Args:
            parent (QWidget): The parent widget.
            stack (QStackedWidget): The current stack of views        
        """
        super().__init__(parent)
        self.stack = stack
        self.setup_ui()


    def setup_ui(self):
        """
        Sets up the user interface for the home page.

        This includes:
        - A title label with bold formatting.
        - A description label with word wrapping.
        - A button to navigate to the form view.
        - A stretch to push content to the top for better alignment.
        """
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
        self.go_to_form_btn.setFixedWidth(100)
        self.go_to_form_btn.clicked.connect(self.go_to_form)
        layout.addWidget(self.go_to_form_btn)

        # Push content to the top for better alignment
        layout.addStretch() 
        self.setLayout(layout)


    def go_to_form(self):
        self.form_page = FormPage(self, self.stack)
        self.stack.addWidget(self.form_page)
        self.stack.setCurrentWidget(self.form_page)