from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QHeaderView, 
    QPushButton, QSizePolicy
)
from PySide6.QtCore import Qt

# Assume that LatexLabel is defined in gui/latex_image_page.py 
# and FGraphicResults is defined in methods/FGraphicResults.py
from gui.latex_image_page import LatexLabel


class FResultsPage(QWidget):
    """
    A QWidget subclass that displays F-based results in a tabular format.
    Each row corresponds to a mode comparison:
        - Row 0: Mode 0 and 1 compared.
        - Row 1: Mode 1 and 2 compared.
    Each column corresponds to an F value (F = 0.2 and F = 0.5).
    Clicking on a cell generates and displays a plot using the FGraphicResults object.
    """
    def __init__(self, parent, stack, n_eff_TE, n_eff_TM, lambd):
        super().__init__(parent)
        self.stack = stack

        # n_eff_TE is an array, e.g. [value_mode0, value_mode1, value_mode2]
        self.n_eff_TE = n_eff_TE  
        self.n_eff_TM = n_eff_TM  # Not used here; adjust if needed.
        self.lambd = lambd

        # Define the F values (columns) and mode comparisons (rows).
        self.F_values = [0.2, 0.5]
        self.num_rows = 2  # Row 0: Mode 0 and 1 compared; Row 1: Mode 1 and 2 compared

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Title label (object name picks up #titleLabel style)
        title = QLabel("Resultados para el parámetro F")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Description label (object name picks up #descriptionLabel style)
        description = QLabel("En esta sección se muestran las curvas de Pa(z) y Pb(z) al fijar el valor de F, lo que permite analizar cómo se transfiere la energía en el acoplamiento óptico entre guías de ondas paralelas. Estos resultados facilitan la comprensión de la eficiencia con la que la luz puede ser controlada y dirigida en dispositivos fotónicos, aspecto esencial para la optimización de circuitos integrados ópticos y acopladores.")
        description.setObjectName("descriptionLabel")
        description.setWordWrap(True)
        main_layout.addWidget(description)

        # Create a table with rows for each mode comparison and columns for each F value.
        self.table = QTableWidget(self.num_rows, len(self.F_values))
        # Horizontal headers: F values.
        self.table.setHorizontalHeaderLabels([f"F = {F}" for F in self.F_values])
        # Vertical headers: mode comparisons.
        self.table.setVerticalHeaderLabels([
            "Mode 0 and 1 compared",
            "Mode 1 and 2 compared"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Apply styling similar to your ResultsPage.
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

        # Populate each cell with a simple label prompting the user to click.
        for row in range(self.num_rows):
            for col, F in enumerate(self.F_values):
                placeholder = QLabel("Click to view plot")
                placeholder.setAlignment(Qt.AlignCenter)
                placeholder.setStyleSheet("""
                    background-color: white;
                    border: 1px solid #a0a0a0;
                    border-radius: 4px;
                    padding: 8px;
                """)
                self.table.setCellWidget(row, col, placeholder)

        # Connect cell clicks to the handler.
        self.table.cellClicked.connect(self.handle_F_cell_clicked)
        main_layout.addWidget(self.table)

        # Create a horizontal layout for navigation buttons.
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        buttons_layout.setContentsMargins(0, 0, 0, 0)

        # "Back" button.
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
        Retrieves the corresponding F value and uses the effective indices
        from n_eff_TE based on the row to generate and display the plot using the FGraphicResults object.
        """
        # Get the F value from the clicked column.
        F_value = self.F_values[column]
        print(f"Cell clicked for F = {F_value}")

        # Use strict +1 indexing:
        # Row 0: Compare mode 0 and 1 → effective indices: n_eff_TE[0] and n_eff_TE[1]
        # Row 1: Compare mode 1 and 2 → effective indices: n_eff_TE[1] and n_eff_TE[2]
        if row == 0:
            effective1 = self.n_eff_TE[0]
            effective2 = self.n_eff_TE[1]
        elif row == 1:
            effective1 = self.n_eff_TE[1]
            effective2 = self.n_eff_TE[2]

        print(f"Using effective indices: {effective1} and {effective2}")

        # Import the FGraphicResults object (assumed defined in methods/FGraphicResults.py).
        from methods.FGraphicResults import FGraphicResults

        # Create an instance of FGraphicResults with the selected effective indices and wavelength.
        f_graphics = FGraphicResults(effective1, effective2, self.lambd)
        # Generate the plot for the selected F value.
        fig = f_graphics.plot_F_graphs(F_value=F_value)
        fig.show()

    def go_back(self):
        """
        Navigates back to the previous page.
        """
        self.stack.removeWidget(self)
