"""
ResultsPage Module

This module defines the ResultsPage class, which displays the results of two
methods: "metodo de rayos" and "metodo ondulatorio." Each method's results
are shown in separate tables with labeled columns and rows.
"""


from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtGui import QFont
from methods.metodo_ondulatorio import metodo_ondulatorio
from methods.metodo_rayos import metodo_rayo


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
        n_t (float): Transverse refractive index.
        h (float): Waveguide height.
        k_0 (float): Free-space wave number.
        lambd (float): Wavelength.
        parent (QWidget, optional): Parent widget. Defaults to None.
    """


    METHODS = ["rayos", "ondulatorio"]
    TITLES = {
        "rayos": "Metodo de rayos", 
        "ondulatorio": "Metodo ondulatorio"
    }
    N = 2 # Number of rows (2 for TE, TM)
    M = 3 # Number of columns (3 for 0,1,2)

    def __init__(self, n_co, n_cl, n_t, h, k_0, lambd, parent=None):
        """
        Initializes the ResultsPage with the given parameters and sets up the UI.

        Args:
            n_co (float): Core refractive index.
            n_cl (float): Cladding refractive index.
            n_t (float): Transverse refractive index.
            h (float): Waveguide height.
            k_0 (float): Free-space wave number.
            lambd (float): Wavelength.
            parent (QWidget, optional): Parent widget. Defaults to None.
        """

        super().__init__(parent)
        
        self.n_co = n_co
        self.n_cl = n_cl
        self.n_t = n_t
        self.h = h
        self.k_0 = k_0
        self.lambd = lambd
        
        self.setup_ui()


    def setup_ui(self):
        """
        Sets up the UI layout, including tables for displaying results.

        Each method has:
        - A title label
        - A description label
        - A results table (2 rows × 3 columns)
        """

        table_layouts = []

        for m in self.METHODS:
            layout_table = QVBoxLayout()
            title = QLabel(self.TITLES[m])
            title.setFont(QFont("Arial", 16, QFont.Bold))
            layout_table.addWidget(title)

            description = QLabel("Description for the rayos column results.")
            description.setWordWrap(True)
            layout_table.addWidget(description)

            table = QTableWidget(2, 3)
            table.setHorizontalHeaderLabels(["0", "1", "2"])
            table.setVerticalHeaderLabels(["TE", "TM"])
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            layout_table.addWidget(table)
            table_layouts.append(layout_table)

            if m == "rayos":
                self.fillTableRayos(table)
            elif m == "ondulatorio":
                self.fillTableOndulatorio(table)

        main_layout = QHBoxLayout(self)

        for layout in table_layouts:
            main_layout.addLayout(layout, 1)

        self.setLayout(main_layout)


    def fillTableRayos(self, table):
        """
        Computes and fills the table with results from the rayos method.

        Args:
            table (QTableWidget): The table to populate.
        """

        results_rayo = metodo_rayo(
            n_co=self.n_co,
            n_t=self.n_t,
            h=self.h,
            k_0=self.k_0,
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
            k_0=self.k_0,
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