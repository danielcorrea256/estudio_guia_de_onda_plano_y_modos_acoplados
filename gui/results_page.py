"""
gui.ResultsPage Module

This module defines the `ResultsPage` class, which displays the results of two numerical methods 
(rayos and ondulatorio) in a tabular format. Each method has its own table showing TE and TM 
values, and for the "rayos" method, additional LaTeX equations for phi are included. 
All content is placed within a QScrollArea for scrollable access, and users can navigate 
to other parts of the application via the provided buttons.
"""


from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, 
    QSizePolicy, QScrollArea
)
from PySide6.QtGui import QIcon
import math

from methods.metodo_ondulatorio import metodo_ondulatorio
from methods.metodo_rayos import metodo_rayo
from gui.latex_util import LatexLabel
from gui.metodos_acoplados_page import MetodosAcopladosPage
from methods.GraphicResults import GraphicResults


class ResultsPage(QWidget):
    """
    A QWidget subclass that displays the results of two numerical methods
    in tabular format, with two additional LaTeX equations (for phi) above
    the first (rayos) table. The entire content is wrapped in a QScrollArea
    for scrolling.
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
        Initializes the ResultsPage with the given waveguide parameters 
        and sets up the user interface.

        Args:
            parent (QWidget): The parent widget.
            stack (QStackedWidget): The widget stack for navigation.
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
        self.alpha_TE = [0] * 3
        self.alpha_TM = [0] * 3
        self.n_eff_TE = [0] * 3
        self.n_eff_TM = [0] * 3
        self.setup_ui()

    def setup_ui(self):
        """
        Sets up the UI layout, including tables for displaying results,
        and a scroll bar. The phi equations appear above the rayos table.
        """
        # 1) Apply a stylesheet removing the color for row/col headers
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: 'Helvetica';
            }
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #dddddd;
                gridline-color: #cccccc;
            }
            QHeaderView::section {
                background-color: #ffffff;
                color: #2c3e50;
                font-weight: bold;
                border: 1px solid #dddddd;
            }
            QPushButton {
                background-color: #2c3e50;
                color: white;
                border-radius: 4px;
                padding: 6px 12px;
                margin: 0px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1f2d3d;
            }
        """)

        # 2) Create a QScrollArea to hold all content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container_widget = QWidget()
        container_layout = QVBoxLayout(container_widget)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(15)

        # 3) Tables layout
        tables_layout = QHBoxLayout()
        table_layouts = []

        for method in self.METHODS:
            layout_table = QVBoxLayout()

            # Title label
            title = QLabel(self.TITLES[method])
            title.setObjectName("titleLabel")
            layout_table.addWidget(title)

            description = QLabel("Vamos a encontrar valores para el ángulo θ que resuelvan la siguiente ecuación")
            description.setWordWrap(True)
            layout_table.addWidget(description)

            # Equation
            main_eq = LatexLabel(self.EQUATIONS[method], fontsize=12)
            layout_table.addWidget(main_eq)

            # Create table
            table = QTableWidget(self.N, self.M)
            table.horizontalHeader().setIconSize(QSize(100, 40))
            table.verticalHeader().setIconSize(QSize(100, 40))

            vertical_headers_items = self.getHeaders(self.VERTICAL_HEADERS, fontsize=18)
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

            # Fill table
            if method == "rayos":
                self.fillTableRayos(table)
            else:
                self.fillTableOndulatorio(table)
                table.cellClicked.connect(self.handle_ondulatorio_cell_clicked)

            # If it's "rayos", show the phi equations ABOVE the table
            if method == "rayos":
                eq_phi_te = LatexLabel(
                    r"$\phi_{TE} = \tan^{-1}[\frac{n_t}{n_i \cos(\theta)} \sqrt{\frac{n_i^2}{n_t^2}\sin^2(\theta) - 1}]$",
                    fontsize=10
                )
                eq_phi_tm = LatexLabel(
                    r"$\phi_{TM} = \tan^{-1}[\frac{n_i}{n_t \cos(\theta)} \sqrt{\frac{n_i^2}{n_t^2}\sin^2(\theta) - 1}]$",
                    fontsize=10
                )
                layout_table.addWidget(eq_phi_te, alignment=Qt.AlignCenter)
                layout_table.addWidget(eq_phi_tm, alignment=Qt.AlignCenter)

        # 4) Add both table layouts side by side
        for layout in table_layouts:
            tables_layout.addLayout(layout)

        container_layout.addLayout(tables_layout)

        # 5) Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        self.submit_btn = QPushButton("Back")
        self.submit_btn.setFixedWidth(100)
        self.submit_btn.clicked.connect(self.go_to_form)
        buttons_layout.addWidget(self.submit_btn)

        self.metodos_btn = QPushButton("Metodos Acoplados")
        self.metodos_btn.setFixedWidth(200)
        self.metodos_btn.clicked.connect(self.go_to_metodos_acoplados)
        buttons_layout.addWidget(self.metodos_btn)

        container_layout.addLayout(buttons_layout)

        # 6) Put container_widget in the scroll area
        scroll_area.setWidget(container_widget)

        # 7) Final layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def getHeaders(self, headers, fontsize=16):
        """
        Converts header LaTeX strings into QTableWidgetItems with icons.

        Args:
            headers (list): A list of LaTeX strings for the table headers.
            fontsize (int): Font size for rendering the LaTeX headers.

        Returns:
            list: A list of QTableWidgetItem objects with LaTeX icons.
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

        Args:
            table (QTableWidget): The table to fill with computed results.
        """
        self.results_rayo = metodo_rayo(
            n_co=self.n_co,
            n_cl=self.n_cl,
            h=self.h,
            lambd=self.lambd,
            ms=range(self.M)
        )
        self.fillTable(table, self.results_rayo)

    def fillTableOndulatorio(self, table):
        """
        Computes and fills the table with results from the ondulatorio method.

        Args:
            table (QTableWidget): The table to fill with computed results.
        """
        self.results_ondulatorio = metodo_ondulatorio(
            n_co=self.n_co,
            n_cl=self.n_cl,
            h=self.h,
            lambd=self.lambd,
            ms=range(self.M)
        )
        self.fillTable(table, self.results_ondulatorio)

    def fillTable(self, table, results):
        """
        Populates the table with numerical results for TE and TM modes.

        Args:
            table (QTableWidget): The table where results are placed.
            results (dict): A dictionary containing "TE" and "TM" lists 
                            with the computed angles.
        """
        for m in range(self.M):
            self.alpha_TE[m] = round(results["TE"][m], 1)
            self.alpha_TM[m] = round(results["TM"][m], 1)
            self.n_eff_TE[m] = round(math.sin(math.radians(self.alpha_TE[m])) * self.n_co, 2)
            self.n_eff_TM[m] = round(math.sin(math.radians(self.alpha_TM[m])) * self.n_co, 2)
            table.setItem(0, m, QTableWidgetItem(str(self.alpha_TE[m])))
            table.setItem(1, m, QTableWidgetItem(str(self.alpha_TM[m])))
            table.setItem(2, m, QTableWidgetItem(str(self.n_eff_TE[m])))
            table.setItem(3, m, QTableWidgetItem(str(self.n_eff_TM[m])))

    def handle_ondulatorio_cell_clicked(self, row, column):
        """
        Handles clicks on cells in the ondulatorio table.

        For the first two rows (row 0 for TE, row 1 for TM), this method 
        generates a pop-up graphic with two plots (E and H fields) corresponding 
        to the clicked mode and m value.

        Args:
            row (int): The row index in the table.
            column (int): The column index in the table.
        """
        if row not in [0, 1]:
            return

        mode = "TE" if row == 0 else "TM"
        m_index = column
        gr = GraphicResults(self.n_co, self.n_cl, self.h, self.lambd)
        fig = gr.plot_fields(mode, m_index)
        fig.show()

    def go_to_form(self):
        """
        Navigates back to the form page.
        """
        self.stack.removeWidget(self)

    def go_to_metodos_acoplados(self):
        """
        Navigates to the Metodos Acoplados page.
        """
        metodos_page = MetodosAcopladosPage(self, self.stack, self.n_eff_TE, self.n_eff_TM, self.lambd)
        self.stack.addWidget(metodos_page)
        self.stack.setCurrentWidget(metodos_page)
