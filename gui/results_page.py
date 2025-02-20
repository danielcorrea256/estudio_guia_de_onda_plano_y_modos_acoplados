"""
ResultsPage Module

This module defines the ResultsPage class, which displays the results of two
methods: "metodo de rayos" and "metodo ondulatorio." Each method's results
are shown in separate tables with labeled columns and rows.
"""


from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QSizePolicy
)
from PySide6.QtGui import QFont
from methods.metodo_ondulatorio import metodo_ondulatorio
from methods.metodo_rayos import metodo_rayo
from gui.latex_image_page import LatexLabel


class ResultsPage(QWidget):
    """
    A QWidget subclass that displays the results of two numerical methods
    in tabular format.

    Attributes:
        METHODS (list[str]): List of methods used in the calculations.
        TITLES (dict): Titles corresponding to each method.
        N (int): Number of rows in the result tables.
        M (int): Number of columns in the result tables.

    Args:
        n_co (float): Core refractive index.
        n_cl (float): Cladding refractive index.
        h (float): Waveguide height.
        lambd (float): Wavelength.
        parent (QWidget, optional): Parent widget. Defaults to None.
    """


    METHODS = ["rayos", "ondulatorio"]
    TITLES = {
        "rayos": "Metodo de rayos", 
        "ondulatorio": "Metodo ondulatorio"
    }
    EQUATIONS = {
        "rayos": r"$2n_{co}k_0hcos(\alpha)-2\phi_s-2\phi_{cl}=2m\pi^2$",
        "ondulatorio": r"$W^2+U^2 =(\frac{k_0 h}{2})^2(n_{co}^2 - n_{cl}^2)$"
    }
    N = 2 # Number of rows (2 for TE, TM)
    M = 3 # Number of columns (3 for 0,1,2)

    def __init__(self, parent, stack, n_co, n_cl, h, lambd):
        """
        Initializes the ResultsPage with the given parameters and sets up the UI.

        Args:
            parent (QWidget): The parent widget.
            stack (QStackedWidget): The current stack of views
            n_co (float): Core refractive index.
            n_cl (float): Cladding refractive index.
            h (float): Waveguide height.
            lambd (float): Wavelength.
        """

        super().__init__(parent)
        
        self.n_co = n_co
        self.n_cl = n_cl
        self.h = h
        self.lambd = lambd
        self.stack = stack
        
        self.setup_ui()


    def setup_ui(self):
        """
        Sets up the UI layout, including tables for displaying results.
        """
        tables_layout = QHBoxLayout()
        table_layouts = []

        for m in self.METHODS:
            layout_table = QVBoxLayout()
            
            title = QLabel(self.TITLES[m])
            title.setFont(QFont("Helvetica", 16, QFont.Bold))
            layout_table.addWidget(title)

            equation = LatexLabel(self.EQUATIONS[m])
            layout_table.addWidget(equation)

            # Create table
            table = QTableWidget(self.N, self.M)
            table.setHorizontalHeaderLabels(["0", "1", "2"])
            table.setVerticalHeaderLabels(["TE", "TM"])
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            # Deactivate scrollbar inside tables
            table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

            # Set size policy: Expand horizontally, but keep a fixed height
            table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
            table.setMaximumHeight(table.verticalHeader().length() + table.horizontalHeader().height() + 10) 

            layout_table.addWidget(table)
            table_layouts.append(layout_table)

            if m == "rayos":
                self.fillTableRayos(table)
            elif m == "ondulatorio":
                self.fillTableOndulatorio(table)

        for layout in table_layouts:
            tables_layout.addLayout(layout)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(tables_layout, stretch=0)

        # Back button, centered
        self.submit_btn = QPushButton("Back")
        self.submit_btn.setFixedWidth(100)
        
        main_layout.addWidget(self.submit_btn, alignment=Qt.AlignCenter)
        self.submit_btn.clicked.connect(self.go_to_form)

        self.setLayout(main_layout)


    def fillTableRayos(self, table):
        """
        Computes and fills the table with results from the rayos method.

        Args:
            table (QTableWidget): The table to populate.
        """

        results_rayo = metodo_rayo(
            n_co=self.n_co,
            n_cl=self.n_cl,
            h=self.h,
            lambd=self.lambd,
            ms=range(self.M)
        )

        self.fillTable(table, results_rayo)

    
    def fillTableOndulatorio(self, table):
        """
        Computes and fills the table with results from the ondulatorio method.

        Args:
            table (QTableWidget): The table to populate.
        """

        results_ondulatorio = metodo_ondulatorio(
            n_co=self.n_co,
            n_cl=self.n_cl,
            h=self.h,
            lambd=self.lambd,
            ms=range(self.M)
        )

        self.fillTable(table, results_ondulatorio)


    def fillTable(self, table, results):
        """
        Populates the table with numerical results.

        Args:
            table (QTableWidget): The table to populate.
            results (dict): A dictionary with keys "TE" and "TM", each containing 
                a list of numerical results for each mode.
        """

        for m in range(self.M):
            numerical_value_TE = round(results["TE"][m], 1)
            numerical_value_TM = round(results["TM"][m], 1)

            tableItem_TE = QTableWidgetItem(str(numerical_value_TE))
            tableItem_TM = QTableWidgetItem(str(numerical_value_TM))

            table.setItem(0, m, tableItem_TE)
            table.setItem(1, m, tableItem_TM)


    def go_to_form(self):
        self.stack.removeWidget(self)

        