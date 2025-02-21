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
from PySide6.QtGui import QFont, QIcon
from methods.metodo_ondulatorio import metodo_ondulatorio
from methods.metodo_rayos import metodo_rayo
from gui.latex_image_page import LatexLabel
import matplotlib
import math

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
    VERTICAL_HEADERS = [
        r"$TE$",
        r"$TM$",
        r"$n_{eff}TE$",
        r"$n_{eff}TM$"
    ]
    HORIZONTAL_HEADERS = [
        r"$0$",
        r"$1$",
        r"$2$"
    ]

    N = 4 # Number of rows
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
            
            # Put headers
            vertical_headers_items = self.getHeaders(self.VERTICAL_HEADERS)
            horizonta_headers_items = self.getHeaders(self.HORIZONTAL_HEADERS)

            for i in range(self.N):
                table.setVerticalHeaderItem(i, vertical_headers_items[i])

            for i in range(self.M):
                table.setHorizontalHeaderItem(i, horizonta_headers_items[i])

            # Deactivate scrollbar inside tables
            table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Stretch to fill width
            table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Stretch to fill width

            # Set size policy: Expand horizontally, but keep a fixed height
            table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            #table.setMaximumHeight(table.verticalHeader().length() + table.horizontalHeader().height() + 10) 

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


    def getHeaders(self, headers):
        headers_items = []

        for h in headers:
            latex_pixmap = LatexLabel.latex_to_pixmap(h)
            item = QTableWidgetItem()
            item.setIcon(QIcon(latex_pixmap))
            headers_items.append(item)

        return headers_items

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
            # extract angle
            alpha_TE = round(results["TE"][m], 1)
            alpha_TM = round(results["TM"][m], 1)

            # Calculate coefficients for the table.
            n_eff_TE = round(math.sin(math.radians(alpha_TE)) * self.n_co, 2)
            n_eff_TM = round(math.sin(math.radians(alpha_TM)) * self.n_co, 2)

            # Create items for the table.
            tableItem_alpha_TE = QTableWidgetItem(str(alpha_TE))
            tableItem_alpha_TM = QTableWidgetItem(str(alpha_TM))
            tableItem_n_TE = QTableWidgetItem(str(n_eff_TE))
            tableItem_n_TM = QTableWidgetItem(str(n_eff_TM))

            # Put items on the table.
            table.setItem(0, m, tableItem_alpha_TE)
            table.setItem(1, m, tableItem_alpha_TM)
            table.setItem(2, m, tableItem_n_TE)
            table.setItem(3, m, tableItem_n_TM)
            

    def go_to_form(self):
        self.stack.removeWidget(self)

        