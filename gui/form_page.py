from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel
from gui.latex_image_page import LatexLabel

class FormPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title_label = QLabel("Form Page")
        layout.addWidget(title_label)

        form_layout = QFormLayout()
        self.n_co_input = QLineEdit()
        self.n_cl_input = QLineEdit()
        self.n_t_input = QLineEdit()
        self.h_input = QLineEdit()
        self.k_0_input = QLineEdit()
        self.lambda_input = QLineEdit()

        n_co_label = LatexLabel(r"$n_{co}$")
        n_cl_label = LatexLabel(r"$n_{cl}$")
        n_t_label = LatexLabel(r"$n_t$")
        h_label = LatexLabel(r"$h$")
        k_0_label = LatexLabel(r"$k_0$")
        lambda_label = LatexLabel(r"$\lambda$")

        form_layout.addRow(n_co_label, self.n_co_input)
        form_layout.addRow(n_cl_label, self.n_cl_input)
        form_layout.addRow(n_t_label, self.n_t_input)
        form_layout.addRow(h_label, self.h_input)
        form_layout.addRow(k_0_label, self.k_0_input)
        form_layout.addRow(lambda_label, self.lambda_input)
        layout.addLayout(form_layout)

        self.submit_btn = QPushButton("Submit")
        layout.addWidget(self.submit_btn)

        layout.addStretch()
