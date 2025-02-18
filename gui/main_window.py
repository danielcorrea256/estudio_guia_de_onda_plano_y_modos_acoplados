"""
Main window for the multi-view PySide6 application.

This module defines the MainWindow class, which manages multiple pages 
using QStackedWidget. It allows navigation between:
- HomePage
- FormPage
- ResultsPage
"""


from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
from gui.home_page import HomePage
from gui.results_page import ResultsPage


class MainWindow(QWidget):
    """
    The main application window that manages different pages using QStackedWidget.

    Attributes:
        stack (QStackedWidget): Stack of views, top is current page.
        home_page (HomePage): The initial home page of the application.
        form_page (FormPage): The page where users input data.
        results_page (ResultsPage): The results page that displays computed output.
    """


    def __init__(self):
        """
        Initializes the main window and sets up the UI components.
        """
        super().__init__()
        self.setWindowTitle("Multi-View Application")
        self.setMinimumSize(800, 600)

        # Create a stacked widget to manage multiple pages
        self.stack = QStackedWidget()

        # Initialize home page
        self.home_page = HomePage(self, self.stack)
        self.stack.addWidget(self.home_page)

        # Set up the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)

        # Apply Stylesheet for more life!
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Helvetica, Arial, sans-serif;
            }

            QLabel {
                font-size: 16px; /* Reduced font size */
                font-weight: bold;
                color: #4a4a4a;
            }

            QPushButton {
                background-color: #7f8c8d;
                color: white;
                border-radius: 4px;
                padding: 6px; /* Smaller padding */
                font-size: 13px;
                border: 1px solid #5e6b6b;
            }

            QPushButton:hover {
                background-color: #707b7c;
            }

            QTableWidget {
                border: 1px solid #a0a0a0;
                background-color: white;
                gridline-color: #c0c0c0;
            }

            QHeaderView::section {
                background-color: #5d6d7e;
                color: white;
                padding: 4px;
                border: none;
                font-weight: bold;
            }

            /* FORM STYLING - Smaller Inputs */
            QLineEdit, QComboBox, QTextEdit, QSpinBox {
                background-color: white;
                border: 1px solid #b0b0b0;
                border-radius: 3px;
                padding: 4px;  /* Reduced padding */
                font-size: 13px; /* Smaller font */
                color: #333;
                min-height: 24px; /* Reduced height */
            }

            QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QSpinBox:focus {
                border: 1px solid #7f8c8d;
            }

            QComboBox::drop-down {
                border-left: 1px solid #b0b0b0;
                width: 18px;
                background-color: #7f8c8d;
            }

            QComboBox::down-arrow {
                image: url(down-arrow.png);
            }

            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #7f8c8d;
                border: none;
                width: 14px;
            }

            QSpinBox::up-arrow, QSpinBox::down-arrow {
                image: url(up-arrow.png);
            }
        """)





    def show_results(self):
        """
        Handles the transition to the results page.

        Steps:
            1. Retrieves user input from the form.
            2. Passes the input data to the ResultsPage.
            3. Displays the results page.

        If input conversion fails, default values are used.

        Raises:
            ValueError: If the form inputs cannot be converted to float.
        """

        # For dev purposes, accept empty inputs
        try:
            n_co = float(self.form_page.n_co_input.text())
            n_cl = float(self.form_page.n_cl_input.text())
            n_t = float(self.form_page.n_t_input.text())
            h = float(self.form_page.h_input.text())
            k_0 = float(self.form_page.k_0_input.text())
            lambd = float(self.form_page.lambda_input.text())

            self.results_page = ResultsPage(n_co, n_cl, n_t, h, k_0, lambd)
        except Exception:
            self.results_page = ResultsPage(1.5, 1, 1, 1, 2, 1)

        # Add and switch to the results page
        self.stack.addWidget(self.results_page)
        self.stack.setCurrentWidget(self.results_page)