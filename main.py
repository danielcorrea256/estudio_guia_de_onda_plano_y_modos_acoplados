"""
Main entry point for the PySide6 application.

This script initializes the application, creates the main window,
and starts the event loop.
"""


import sys
from gui.main_window import MainWindow
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("logo.png"))  

    # Instantiate and display the main window
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
