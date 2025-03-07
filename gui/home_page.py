"""
gui.HomePage Module

This module defines the `HomePage` class, which serves as the main landing page 
for a PySide6 GUI application. It displays a title, a brief description, and a 
button to navigate to the form page.
"""


from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton
)
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
        stack (QStackedWidget): The current stack of views for navigation.
    """

    # Title shown at the top of the page
    TITLE = "Proyecto Estudio Guía de Onda Plano y Modos Acoplados"

    # Description text providing an overview of the application's purpose
    DESCRIPTION = """Esta aplicación está diseñada para calcular los modos de propagación en una guía de onda plano.\nEl programa ofrece dos enfoques para el análisis: el método de rayos y el análisis ondulatorio.\nPara resolver las ecuaciones trascendentes que surgen al aplicar la teoría tanto de rayos como ondulatoria, implementamos el método numérico de bisección, lo que nos permite encontrar soluciones de manera eficiente y precisa.\nEste método es fundamental para encontrar los valores de los modos de propagación que no se pueden obtener directamente de manera analítica, al obtener los modos, se encuentran otros parámetros que son fundamentales para el estudio del guía de onda."""

    def __init__(self, parent, stack):
        """
        Initializes the HomePage with a title, description, and navigation button.

        Args:
            parent (QWidget): The parent widget.
            stack (QStackedWidget): The current stack of views.
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
        title_label = QLabel(self.TITLE)
        title_label.setObjectName("titleLabel")
        layout.addWidget(title_label)

        # Description Label
        description_label = QLabel(self.DESCRIPTION)
        description_label.setObjectName("descriptionLabel")
        description_label.setWordWrap(True)
        layout.addWidget(description_label)

        # Button to switch to the Form view
        self.go_to_form_btn = QPushButton("Entrada de datos")
        self.go_to_form_btn.setFixedWidth(150)
        self.go_to_form_btn.clicked.connect(self.go_to_form)
        layout.addWidget(self.go_to_form_btn)

        # Push content to the top for better alignment
        layout.addStretch() 
        self.setLayout(layout)

    def go_to_form(self):
        """
        Creates an instance of FormPage and navigates the user to it 
        by adding it to the stack and setting it as the current widget.
        """
        self.form_page = FormPage(self, self.stack)
        self.stack.addWidget(self.form_page)
        self.stack.setCurrentWidget(self.form_page)
