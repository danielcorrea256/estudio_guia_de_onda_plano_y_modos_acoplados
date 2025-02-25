"""
ResultsPage Module

This module defines the ResultsPage class, which displays the results of two
numerical methods: "metodo de rayos" and "metodo ondulatorio." Each method's results
are shown in separate tables with labeled columns and rows.
"""

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QSizePolicy,
    QGraphicsView, QGraphicsScene, QGraphicsProxyWidget, QGraphicsRectItem
)
from PySide6.QtGui import QBrush, QColor, QFont, QIcon
from methods.metodo_ondulatorio import metodo_ondulatorio
from methods.metodo_rayos import metodo_rayo
from gui.latex_image_page import LatexLabel
import math

class TableGraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(self.renderHints() | QGraphicsView.Antialiasing)

        # Define table size
        rows, cols = 2, 2
        cell_width, cell_height = 150, 80
        start_x, start_y = 50, 50  # Positioning

        # Define headers with LaTeX equations (using a larger fontsize)
        headers = [
            r"$\nabla^2 u = 0$",  # Laplace equation
            r"$\frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} = 0$"
        ]

        # Add header row
        for col, header_text in enumerate(headers):
            latex_label = LatexLabel(header_text, fontsize=16)
            proxy = self.scene().addWidget(latex_label)
            proxy.setPos(start_x + col * cell_width, start_y)

        # Add data cells
        for row in range(rows):
            for col in range(cols):
                rect = QGraphicsRectItem(start_x + col * cell_width, start_y + (row + 1) * cell_height,
                                         cell_width, cell_height)
                rect.setBrush(QBrush(QColor(220, 220, 220)))
                rect.setPen(QColor(0, 0, 0))
                self.scene().addItem(rect)

                # Sample text inside cells
                label = QLabel(f"({row},{col})")
                proxy = QGraphicsProxyWidget()
                proxy.setWidget(label)
                proxy.setPos(start_x + col * cell_width + 50, start_y + (row + 1) * cell_height + 20)
                self.scene().addItem(proxy)


class ResultsPage(QWidget):
    """
    A QWidget subclass that displays the results of two numerical methods
    in tabular format.
    """

    METHODS = ["rayos", "ondulatorio"]
    TITLES = {
        "rayos": "Metodo de rayos", 
        "ondulatorio": "Metodo ondulatorio"
    }
    EQUATIONS = {
        "rayos": r"$2n_{co}k_0h\cos(\theta)-2\phi_s-2\phi_{cl}=2m\pi^2$",
        "ondulatorio": r"$W^2+U(\theta)^2 =\left(\frac{k_0 h}{2}\right)^2(n_{co}^2 - n_{cl}^2)$"
    }
    VERTICAL_HEADERS = [
        r"$TE$",
        r"$TM$",
        r"$n_{eff}^{TE}$",
        r"$n_{eff}^{TM}$"
    ]
    HORIZONTAL_HEADERS = [
        "m=0",
        "m=1",
        "m=2"
    ]

    N = 4  # Number of rows
    M = 3  # Number of columns

    def __init__(self, parent: QWidget, stack, n_co, n_cl, h, lambd):
        """
        Initializes the ResultsPage with the given parameters and sets up the UI.
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

            # Render equation with a larger fontsize
            equation = LatexLabel(self.EQUATIONS[m], fontsize=12)
            layout_table.addWidget(equation)

            description = QLabel("Vamos a encontrar valores para el ángulo theta que resuelvan la siguiente ecuación")
            description.setWordWrap(True)
            layout_table.addWidget(description)

            # Create table and set header icon sizes
            table = QTableWidget(self.N, self.M)
            table.horizontalHeader().setIconSize(QSize(100, 40))
            table.verticalHeader().setIconSize(QSize(100, 40))

            # Use our custom getHeaders function with an increased fontsize.
            vertical_headers_items = self.getHeaders(self.VERTICAL_HEADERS, fontsize=12)

            for i in range(self.N):
                table.setVerticalHeaderItem(i, vertical_headers_items[i])
            for i in range(self.M):
                table.setHorizontalHeaderItem(i, QTableWidgetItem(self.HORIZONTAL_HEADERS[i]))

            table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

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

        footnote = QLabel("Las columnas representan el valor para m que se toma")
        footnote.setMinimumWidth(500)
        footnote.setWordWrap(True)
        main_layout.addWidget(footnote)

        self.submit_btn = QPushButton("Back")
        self.submit_btn.setFixedWidth(100)
        main_layout.addWidget(self.submit_btn, alignment=Qt.AlignCenter)
        self.submit_btn.clicked.connect(self.go_to_form)

        self.setLayout(main_layout)

    def getHeaders(self, headers, fontsize=16):
        """
        Converts header LaTeX strings into QTableWidgetItems with larger icons.
        """
        headers_items = []
        for h in headers:
            latex_pixmap = LatexLabel.latex_to_pixmap(h, fontsize=fontsize)
            item = QTableWidgetItem()
            item.setIcon(QIcon(latex_pixmap))
            headers_items.append(item)
        return headers_items

    def fillTableRayos(self, table):
        """
        Computes and fills the table with results from the rayos method.
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
        """
        for m in range(self.M):
            alpha_TE = round(results["TE"][m], 1)
            alpha_TM = round(results["TM"][m], 1)
            n_eff_TE = round(math.sin(math.radians(alpha_TE)) * self.n_co, 2)
            n_eff_TM = round(math.sin(math.radians(alpha_TM)) * self.n_co, 2)
            table.setItem(0, m, QTableWidgetItem(str(alpha_TE)))
            table.setItem(1, m, QTableWidgetItem(str(alpha_TM)))
            table.setItem(2, m, QTableWidgetItem(str(n_eff_TE)))
            table.setItem(3, m, QTableWidgetItem(str(n_eff_TM)))

    def go_to_form(self):
        """
        Navigates back to the form page.
        """
        self.stack.removeWidget(self)
