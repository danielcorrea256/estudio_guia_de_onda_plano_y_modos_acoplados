from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView
)

from PySide6.QtGui import QFont
from methods.metodo_ondulatorio import metodo_ondulatorio
from methods.metodo_rayos import metodo_rayo

class ResultsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)

        # ---------------------------
        # rayos Column
        # ---------------------------
        self.rayos_layout = QVBoxLayout()
        self.rayos_title = QLabel("rayos Column Title")
        self.rayos_title.setFont(QFont("Arial", 16, QFont.Bold))
        self.rayos_layout.addWidget(self.rayos_title)

        self.rayos_desc = QLabel("Description for the rayos column results.")
        self.rayos_desc.setWordWrap(True)
        self.rayos_layout.addWidget(self.rayos_desc)

        self.rayos_table = QTableWidget(4, 3)
        self.rayos_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.rayos_table.verticalHeader().setVisible(False)
        self.rayos_layout.addWidget(self.rayos_table)

        # ---------------------------
        # ondulatorio Column
        # ---------------------------
        self.ondulatorio_layout = QVBoxLayout()
        self.ondulatorio_title = QLabel("ondulatorio Column Title")
        self.ondulatorio_title.setFont(QFont("Arial", 16, QFont.Bold))
        self.ondulatorio_layout.addWidget(self.ondulatorio_title)

        self.ondulatorio_desc = QLabel("Description for the ondulatorio column results.")
        self.ondulatorio_desc.setWordWrap(True)
        self.ondulatorio_layout.addWidget(self.ondulatorio_desc)

        self.ondulatorio_table = QTableWidget(4, 3)
        self.ondulatorio_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ondulatorio_table.verticalHeader().setVisible(False)
        self.ondulatorio_layout.addWidget(self.ondulatorio_table)

        # Add both columns to the main layout with equal stretch
        main_layout.addLayout(self.rayos_layout, 1)
        main_layout.addLayout(self.ondulatorio_layout, 1)

        self.setLayout(main_layout)

    def set_data(self, n_co, n_cl, n_t, h, k_0, lambd):
        """
        Update the ResultsPage with data from the form.
        You can display them in labels, tables, etc.
        """

        ms = range(3)

        results_rayo = metodo_rayo(
            n_co=n_co,
            n_t=n_t,
            h=h,
            k_0=k_0,
            ms=ms
        )

        results_ondulatorio = metodo_ondulatorio(
            n_co=n_co,
            n_cl=n_cl,
            h=h,
            k_0=k_0,
            lambd=lambd,
            ms=ms
        )
        
        # Example: Put each piece of data in the rayos table
        #self.rayos_table.setItem(0, 0, QTableWidgetItem(data1))
        #self.rayos_table.setItem(1, 0, QTableWidgetItem(data2))
        #self.rayos_table.setItem(2, 0, QTableWidgetItem(data3))
        #self.rayos_table.setItem(3, 0, QTableWidgetItem(data4))

        # You could also fill the ondulatorio table, or do something else with the data
        #self.ondulatorio_table.setItem(0, 0, QTableWidgetItem("Some computed result"))
