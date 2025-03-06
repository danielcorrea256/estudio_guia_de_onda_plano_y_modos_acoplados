from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

# Assume that LatexLabel is defined in gui/latex_image_page.py and FGraphicResults is defined in methods/FGraphicResults.py
from gui.latex_image_page import LatexLabel


class FResultsPage(QWidget):
    """
    A QWidget subclass that displays F-based results in a tabular format.
    Each column corresponds to a particular F value.
    Clicking on a cell generates and displays a plot using the FGraphicResults object.
    """
    def __init__(self, parent, stack):
        super().__init__(parent)
        self.stack = stack

        # Hardcoded effective indices and wavelength for now.
        self.n_eff1 = 1.45
        self.n_eff2 = 1.29
        self.lambd = 1.0

        # Define the F values to display (columns in the table).
        self.F_values = [0.2, 0.5]
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Title label styled via stylesheet (object name picks up #titleLabel style)
        title = QLabel("F Results")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Description label styled via stylesheet (#descriptionLabel)
        description = QLabel("Click on a cell to view the plot for the corresponding F value.")
        description.setObjectName("descriptionLabel")
        description.setWordWrap(True)
        main_layout.addWidget(description)

        # Create a table with 1 row and columns equal to the number of F values.
        self.table = QTableWidget(1, len(self.F_values))
        self.table.setHorizontalHeaderLabels([f"F = {F}" for F in self.F_values])
        self.table.setVerticalHeaderLabels([""])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Apply inline styling similar to ResultsPage (and consistent with your global stylesheet)
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #a0a0a0;
                background-color: white;
                gridline-color: #c0c0c0;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 5px;
                border: 1px solid #dcdcdc;
                font-weight: bold;
            }
        """)

        # Populate the table with placeholder labels for each F value.
        for col, F in enumerate(self.F_values):
            placeholder = QLabel(f"F = {F}")
            placeholder.setAlignment(Qt.AlignCenter)
            placeholder.setStyleSheet("""
                background-color: white;
                border: 1px solid #a0a0a0;
                border-radius: 4px;
                padding: 8px;
            """)
            self.table.setCellWidget(0, col, placeholder)

        # Connect the cellClicked signal to a handler.
        self.table.cellClicked.connect(self.handle_F_cell_clicked)
        main_layout.addWidget(self.table)

        # Create a horizontal layout for navigation buttons.
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        buttons_layout.setContentsMargins(0, 0, 0, 0)

        # "Back" button to return to the previous page.
        back_btn = QPushButton("Back")
        back_btn.setFixedWidth(100)
        back_btn.setStyleSheet("QPushButton { margin: 0px; padding: 8px 12px; }")
        back_btn.clicked.connect(self.go_back)
        buttons_layout.addWidget(back_btn)

        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

    def handle_F_cell_clicked(self, row, column):
        """
        Handles a click on a cell in the table.
        Retrieves the corresponding F value and uses an FGraphicResults object to
        generate and display the plot.
        """
        # Retrieve the F value for the clicked cell (column).
        F_value = self.F_values[column]
        print(f"Cell clicked for F = {F_value}")

        # Import the FGraphicResults object (assumed defined in methods/FGraphicResults.py).
        from methods.FGraphicResults import FGraphicResults

        # Create an instance of FGraphicResults with hardcoded effective indices and wavelength.
        f_graphics = FGraphicResults(self.n_eff1, self.n_eff2, self.lambd)
        # Generate the plot for the selected F value (pass it as a single-item list).
        fig = f_graphics.plot_F_graphs(F_values=[F_value])
        fig.show()

    def go_back(self):
        """
        Navigates back to the previous page.
        """
        self.stack.removeWidget(self)
