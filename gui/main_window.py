"""
Main window for the multi-view PySide6 application.

This module defines the MainWindow class, which manages multiple pages 
using QStackedWidget. It allows navigation between:
- HomePage
- FormPage
- ResultsPage
- FResultsPage
- MetodosAcopladosPage
"""


from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
from gui.home_page import HomePage
from PySide6.QtGui import QIcon


class MainWindow(QWidget):
    """
    The main application window that manages different pages using QStackedWidget.

    Attributes:
        stack (QStackedWidget): Stack of views, with the top one being the current page.
        home_page (HomePage): The initial home page of the application.
        form_page (FormPage): The page where users input data (instantiated on demand).
        results_page (ResultsPage): The results page that displays computed output (instantiated on demand).
    """

    def __init__(self):
        """
        Initializes the main window and sets up the UI components.

        Steps:
            1. Sets the window title, icon, and minimum size.
            2. Creates a QStackedWidget to hold multiple pages.
            3. Instantiates the HomePage and adds it to the stack.
            4. Applies a layout containing the stacked widget.
            5. Applies a global stylesheet for a consistent look and feel.
        """
        super().__init__()
        self.setWindowTitle("egdopyma")                # Window title
        self.setWindowIcon(QIcon("logo.png"))          # Window icon
        self.setMinimumSize(800, 600)                  # Minimum window size

        # Create a stacked widget to manage multiple pages
        self.stack = QStackedWidget()

        # Initialize the home page and add it to the stack
        self.home_page = HomePage(self, self.stack)
        self.stack.addWidget(self.home_page)

        # Set up the layout to hold the stacked widget
        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)

        # Apply a stylesheet for a modern UI appearance
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Helvetica, Arial, sans-serif;
            }

            QPushButton {
                background-color: #2c3e50; /* Darker grayish-blue */
                color: white;
                border-radius: 6px; /* Slightly rounded corners */
                padding: 8px 12px; /* Comfortable padding */
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #1f2d3d; /* Even darker border for contrast */
                margin: 0px;            
               }

            QPushButton:hover {
                background-color: #1f2d3d; /* Darker shade on hover */
                border-color: #0f1a24;
            }

            QPushButton:pressed {
                background-color: #0f1a24; /* Even darker shade when pressed */
                border-color: #0a121a;
            }

            QPushButton:disabled {
                background-color: #7f8c8d; /* Muted gray when disabled */
                border-color: #5e6b6b;
                color: #bdc3c7;
            }

            QTableWidget {
                border: 1px solid #a0a0a0;
                background-color: white;
                gridline-color: #c0c0c0;
            }

            QHeaderView::section {
                background-color: #f0f0f0; /* Light gray background */
                padding: 5px;
                border: 1px solid #dcdcdc;
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
                           
            #titleLabel {
                font-size: 16px; /* Larger and more prominent */
                font-weight: 700; /* Stronger bold */
                color: #2c3e50; /* Darker shade for better contrast */
                text-align: center; /* Center the title */
                padding: 10px 0; /* Adds spacing around */
                letter-spacing: 1px; /* Slight spacing for readability */
                text-transform: uppercase; /* Gives a more defined look */
            }

            #descriptionLabel {
                font-weight: normal;
                font-size: 16px;
                line-height: 1.5em;
                margin-bottom: 12px;
            }
        """)
