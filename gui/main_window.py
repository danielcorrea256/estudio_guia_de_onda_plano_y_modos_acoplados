"""
Main window for the multi-view PySide6 application.

This module defines the MainWindow class, which manages multiple pages 
using QStackedWidget. It allows navigation between:
- HomePage
- FormPage
- ResultsPage
"""


import sys
from PySide6.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout
from gui.home_page import HomePage
from gui.form_page import FormPage
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
        self.setMinimumSize(1200, 800)

        # Create a stacked widget to manage multiple pages
        self.stack = QStackedWidget()

        # Initialize pages
        self.home_page = HomePage()
        self.form_page = FormPage()

        # Add pages to the stack
        self.stack.addWidget(self.home_page)    # index 0
        self.stack.addWidget(self.form_page)    # index 1

        # Set up the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)

        # Connect buttons for navigation
        self.home_page.go_to_form_btn.clicked.connect(self.show_form)
        self.form_page.submit_btn.clicked.connect(self.show_results)


    def show_form(self):
        """
        Switches the view to the form page.
        """
        self.stack.setCurrentWidget(self.form_page)


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