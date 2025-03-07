"""
FormPage Module

This module defines the `FormPage` class, which represents a user input form 
for numerical parameters, using both standard QLabel and LaTeX-rendered labels.

Overview:
    - Provides an interface for entering waveguide-related parameters (n_co, n_cl, h, λ).
    - Validates user input and navigates to the ResultsPage upon submission.
    - Includes a back button to return to the previous page.
    - Uses LaTeX labels for enhanced readability of mathematical notation.
"""


from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel,
    QHBoxLayout, QMessageBox
)
from gui.latex_util import LatexLabel
from gui.results_page import ResultsPage


class FormPage(QWidget):
    """
    A QWidget subclass that provides a form for user input.

    This form allows users to enter numerical values for different parameters, 
    using LaTeX-rendered labels for better readability of mathematical notation.

    Args:
        parent (QWidget): The parent widget.
        stack (QStackedWidget): The current stack of views.
    """

    def __init__(self, parent, stack):
        """
        Initializes the FormPage with input fields and a submit button.

        Args:
            parent (QWidget): The parent widget.
            stack (QStackedWidget): The stack of views used for navigation.
        """
        super().__init__(parent)
        self.stack = stack
        self.setup_ui()

    def setup_ui(self):
        """
        Sets up the user interface for the form page.

        This includes:
        - A title label with larger, bold text.
        - A form layout containing labeled input fields (n_co, n_cl, h, λ).
        - A pair of navigation buttons (Back and Submit).
        """
        layout = QVBoxLayout(self)

        # Title label
        title_label = QLabel("Datos del problema")
        title_label.setFont(QFont("Helvetica", 26, QFont.Bold))  # Larger, bold font
        title_label.setAlignment(Qt.AlignCenter)                 # Center the text
        title_label.setStyleSheet("color: #2C3E50;")             # Dark blue-gray color for elegance
        title_label.setContentsMargins(0, 20, 0, 20)             # Add spacing around
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Form layout for parameter inputs
        form_layout = QFormLayout()
        self.n_co_input = QLineEdit()
        self.n_cl_input = QLineEdit()
        self.h_input = QLineEdit()
        self.lambda_input = QLineEdit()

        # Labels with LaTeX formatting for clarity
        n_co_label = LatexLabel(r"$n_{co}$")
        n_cl_label = LatexLabel(r"$n_{cl}$")
        h_label = LatexLabel(r"$h (\mu m)$")
        lambda_label = LatexLabel(r"$\lambda (\mu m)$")

        # Add labeled input fields to the form layout
        form_layout.addRow(n_co_label, self.n_co_input)
        form_layout.addRow(n_cl_label, self.n_cl_input)
        form_layout.addRow(h_label, self.h_input)
        form_layout.addRow(lambda_label, self.lambda_input)
        layout.addLayout(form_layout)

        # Create a horizontal layout for the buttons
        buttons_layout = QHBoxLayout()

        # Back button
        self.back_btn = QPushButton("Back")
        self.back_btn.setFixedWidth(100)
        buttons_layout.addWidget(self.back_btn)
        self.back_btn.clicked.connect(self.go_to_homepage)

        # Submit button
        self.submit_btn = QPushButton("Submit")
        self.submit_btn.setFixedWidth(100)
        buttons_layout.addWidget(self.submit_btn)
        self.submit_btn.clicked.connect(self.go_to_results)

        # Center the buttons horizontally
        buttons_layout.setAlignment(Qt.AlignCenter)

        # Add the button layout to the main layout
        layout.addLayout(buttons_layout)

    def go_to_results(self):
        """
        Attempts to parse the user input and navigate to the results page.

        Raises:
            AssertionError: If n_co <= n_cl, displays an error message.
            ValueError: If any input is invalid, displays an error message.
        """
        try:
            n_co = float(self.n_co_input.text())
            n_cl = float(self.n_cl_input.text())
            h = float(self.h_input.text())
            lambd = float(self.lambda_input.text())
            
            assert n_co > n_cl, "The condition n_co > n_cl should hold."

            # Create and display the ResultsPage
            self.results_page = ResultsPage(self, self.stack, n_co, n_cl, h, lambd)
            self.stack.addWidget(self.results_page)
            self.stack.setCurrentWidget(self.results_page)

        except AssertionError:
            QMessageBox.critical(self, "Error!", "The condition n_co > n_cl should hold.", QMessageBox.Ok)
        except ValueError as e:
            print(e)
            QMessageBox.critical(self, "Error!", "The current values are not valid, check your input", QMessageBox.Ok)

    def go_to_homepage(self):
        """
        Removes this page from the stack, returning to the previous page.
        """
        self.stack.removeWidget(self)
