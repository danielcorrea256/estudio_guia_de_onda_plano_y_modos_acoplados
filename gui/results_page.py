from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView
)

from PySide6.QtGui import QFont
from methods.metodo_ondulatorio import metodo_ondulatorio
from methods.metodo_rayos import metodo_rayo


class ResultsPage(QWidget):
    METHODS = ["rayos", "ondulatorio"]

    TITLES = {
        "rayos": "Metodo de rayos", 
        "ondulatorio": "Metodo ondulatorio"
    }

    N = 2
    M = 3

    def __init__(self, n_co, n_cl, n_t, h, k_0, lambd, parent=None):
        super().__init__(parent)
        
        self.n_co = n_co
        self.n_cl = n_cl
        self.n_t = n_t
        self.h = h
        self.k_0 = k_0
        self.lambd = lambd
        
        self.setup_ui()

    def setup_ui(self):

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
        results_rayo = metodo_rayo(
            n_co=self.n_co,
            n_t=self.n_t,
            h=self.h,
            k_0=self.k_0,
            ms=range(self.M)
        )

        self.fillTable(table, results_rayo)

    
    def fillTableOndulatorio(self, table):
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
        for m in range(self.M):
            numerical_value_TE = round(results["TE"][m], 1)
            numerical_value_TM = round(results["TM"][m], 1)

            tableItem_TE = QTableWidgetItem(str(numerical_value_TE))
            tableItem_TM = QTableWidgetItem(str(numerical_value_TM))

            table.setItem(0, m, tableItem_TE)
            table.setItem(1, m, tableItem_TM)