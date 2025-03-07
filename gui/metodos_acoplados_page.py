"""
MetodosAcopladosPage Module

This module defines the `MetodosAcopladosPage` class, which displays a description 
and a set of LaTeX equations related to acoplados (coupled waveguides). The page 
provides buttons for navigating back to the previous page or moving on to view 
F-based results.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
    )
from PySide6.QtCore import Qt
from gui.latex_util import LatexLabel  # Utility for rendering LaTeX
from gui.F_results_page import FResultsPage

class MetodosAcopladosPage(QWidget):
    """
    A QWidget subclass representing the Metodos Acoplados page.
    """

    DESCRIPTION = """En esta etapa del proyecto se analizó el fenómeno de acoplamiento  óptico entre dos guías de ondas paralelas mediante simulaciones, con el objetivo de comprender cómo se transfiere la energía entre ellas dependiendo de diversos  parámetros físicos como la distancia de separación, la longitud de interacción y las propiedades refractivas de los materiales involucrados. El estudio del acoplamiento permitió determinar la eficiencia con la que la luz puede ser controlada y dirigida en dispositivos fotónicos, lo cual es esencial para la optimización del diseño de circuitos integrados ópticos y acopladores ópticos."""

    def __init__(self, parent, stack, n_eff_TE, n_eff_TM, lambd):
        """
        Initializes the MetodosAcopladosPage.

        Args:
            parent (QWidget): The parent widget.
            stack (QStackedWidget): The widget stack used for page navigation.
            n_eff_TE (list): Array of effective indices for TE modes.
            n_eff_TM (list): Array of effective indices for TM modes.
            lambd (float): The wavelength parameter.
        """
        super().__init__(parent)
        self.stack = stack
        self.n_eff_TE = n_eff_TE
        self.n_eff_TM = n_eff_TM
        self.lambd = lambd
        self.setup_ui()

    def setup_ui(self):
        """
        Sets up the user interface elements for the Metodos Acoplados page.
        """
        # Apply a simple stylesheet for the title/description
        self.setStyleSheet("""
            #titleLabel {
                font-size: 22px;
                font-weight: bold;
                color: #2C3E50;
                margin-bottom: 8px;
            }
            #descriptionLabel {
                font-size: 16px;
                line-height: 1.5em;
                margin-bottom: 12px;
            }
        """)

        # Main vertical layout with margins and spacing
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        # Title label for the page
        title = QLabel("Metodos Acoplados")
        title.setObjectName("titleLabel")  # Picks up the stylesheet
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Description label showing the explanation of acoplados
        description_label = QLabel(self.DESCRIPTION)
        description_label.setObjectName("descriptionLabel")
        description_label.setWordWrap(True)
        main_layout.addWidget(description_label)

        # Create an HBox to hold two columns of equations
        equations_layout = QHBoxLayout()

        # Left column for the first half of the equations
        left_col = QVBoxLayout()
        # Right column for the second half of the equations
        right_col = QVBoxLayout()

        # Create LatexLabels for each equation
        equation1 = LatexLabel(r"$P_a(z) = 1 - F \sin^2(\psi z)$", fontsize=14)
        equation2 = LatexLabel(r"$P_b(z) = F \sin^2(\psi z)$", fontsize=14)
        equation3 = LatexLabel(r"$\psi = \sqrt{\kappa^2 + \delta^2}$", fontsize=14)
        equation4 = LatexLabel(r"$\beta = n_{eff} \frac{2\pi}{\lambda_0}$", fontsize=14)
        equation5 = LatexLabel(r"$L_c = \frac{\pi}{2 \psi}$", fontsize=14)
        equation6 = LatexLabel(r"$F = \frac{1}{1 + (\frac{\delta}{\kappa})^2}$", fontsize=14)
        equation7 = LatexLabel(r"$\delta = \frac{\beta_2 - \beta_1}{2}$", fontsize=14)

        # Add some equations to the left column
        left_col.addWidget(equation1, alignment=Qt.AlignCenter)
        left_col.addWidget(equation2, alignment=Qt.AlignCenter)
        left_col.addWidget(equation3, alignment=Qt.AlignCenter)
        left_col.addWidget(equation4, alignment=Qt.AlignCenter)
        # Stretch to push them toward the top
        left_col.addStretch()

        # Add remaining equations to the right column
        right_col.addWidget(equation5, alignment=Qt.AlignCenter)
        right_col.addWidget(equation6, alignment=Qt.AlignCenter)
        right_col.addWidget(equation7, alignment=Qt.AlignCenter)
        right_col.addStretch()

        # Add both columns to the equations layout
        equations_layout.addLayout(left_col)
        equations_layout.addLayout(right_col)

        # Add the equations layout to the main layout
        main_layout.addLayout(equations_layout)

        # Create a horizontal layout for the navigation buttons
        buttons_layout = QHBoxLayout()

        # 'Back' button to return to the previous page
        back_btn = QPushButton("Back")
        back_btn.setFixedWidth(100)
        back_btn.clicked.connect(self.go_back)
        buttons_layout.addWidget(back_btn)

        # 'Graphics' button to navigate to F-based results
        graphics_btn = QPushButton("Graphics")
        graphics_btn.setFixedWidth(100)
        graphics_btn.clicked.connect(self.show_graphics)
        buttons_layout.addWidget(graphics_btn)

        # Add the button layout to the main layout
        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

    def go_back(self):
        """
        Navigates back to the previous page in the stack.
        """
        self.stack.removeWidget(self)

    def show_graphics(self):
        """
        Placeholder for showing a new page with F-based results.
        Creates an instance of FResultsPage and sets it as the current view.
        """
        f_results_page = FResultsPage(self, self.stack, self.n_eff_TE, self.n_eff_TM, self.lambd)
        self.stack.addWidget(f_results_page)
        self.stack.setCurrentWidget(f_results_page)
