"""
FormPage Module

This module defines the `FormPage` class, which represents a user input form 
for numerical parameters, using both standard QLabel and LaTeX-rendered labels.
"""


from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel,
    QSpacerItem, QSizePolicy, QHBoxLayout, QMessageBox
)

from gui.latex_image_page import LatexLabel
from gui.results_page import ResultsPage


class FormPage(QWidget):
    """
    A QWidget subclass that provides a form for user input.

    This form allows users to enter numerical values for different parameters, 
    using LaTeX-rendered labels for better readability of mathematical notation.

    Args:
        parent (QWidget, optional): The parent widget. Defaults to None.
    """


    def __init__(self, parent, stack):
        """
        Initializes the FormPage with input fields and a submit button.

        Args:
            parent (QWidget): The parent widget.
            stack (QStackedWidget): The current stack of views
        """
        super().__init__(parent)
        self.stack = stack
        self.setup_ui()


    def setup_ui(self):
        """
        Sets up the user interface for the form page.

        This includes:
        - A title label.
        - A form layout with labeled input fields for parameters.
        - A submit button.
        - A stretch at the bottom to maintain spacing.
        """
        layout = QVBoxLayout(self)

        # Title label
        title_label = QLabel("Datos del problema")
        title_label.setFont(QFont("Helvetica", 26, QFont.Bold))  # Larger, bold font
        title_label.setAlignment(Qt.AlignCenter)  # Center the text
        title_label.setStyleSheet("color: #2C3E50;")  # Dark blue-gray color for elegance
        title_label.setContentsMargins(0, 20, 0, 20)  # Add spacing around

        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Form layout
        form_layout = QFormLayout()
        self.n_co_input = QLineEdit()
        self.n_cl_input = QLineEdit()
        self.h_input = QLineEdit()
        self.lambda_input = QLineEdit()

        # Labels with LaTeX formatting
        n_co_label = LatexLabel(r"$n_{co}$")
        n_cl_label = LatexLabel(r"$n_{cl}$")
        h_label = LatexLabel(r"$h (\mu m)$")
        lambda_label = LatexLabel(r"$\lambda (\mu m)$")

        # Adding labeled input fields to the form layout
        form_layout.addRow(n_co_label, self.n_co_input)
        form_layout.addRow(n_cl_label, self.n_cl_input)
        form_layout.addRow(h_label, self.h_input)
        form_layout.addRow(lambda_label, self.lambda_input)
        layout.addLayout(form_layout)

        # Create a horizontal layout for the buttons
        buttons_layout = QHBoxLayout()

        # Submit button
        self.submit_btn = QPushButton("Submit")
        self.submit_btn.setFixedWidth(100)
        buttons_layout.addWidget(self.submit_btn)
        self.submit_btn.clicked.connect(self.go_to_results)

        # Back button
        self.back_btn = QPushButton("Back")
        self.back_btn.setFixedWidth(100)
        buttons_layout.addWidget(self.back_btn)
        self.back_btn.clicked.connect(self.go_to_homepage)

        # Align buttons to the center
        buttons_layout.setAlignment(Qt.AlignCenter)

        # Add the button layout to the main layout
        layout.addLayout(buttons_layout)

    
    def go_to_results(self):        
        # For dev purposes, accept empty inputs
        try:
            n_co = float(self.form_page.n_co_input.text())
            n_cl = float(self.form_page.n_cl_input.text())
            h = float(self.form_page.h_input.text())
            lambd = float(self.form_page.lambda_input.text())
            self.results_page = ResultsPage(self, self.stack, n_co, n_cl, h, lambd)
            assert n_co > n_cl

            # Add and switch to the results page
            self.stack.addWidget(self.results_page)
            self.stack.setCurrentWidget(self.results_page)
        except AssertionError:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Warning")
            msg_box.setText("n_co shoulg be bigger than n_cl")
            msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            result = msg_box.exec()
        except Exception:
            self.results_page = ResultsPage(self, self.stack, 1.5, 1, 1, 1)

            # Add and switch to the results page
            self.stack.addWidget(self.results_page)
            self.stack.setCurrentWidget(self.results_page)


    def go_to_homepage(self):
        self.stack.removeWidget(self)
