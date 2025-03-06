from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from gui.latex_image_page import LatexLabel  # Utility for rendering LaTeX
from gui.F_results_page import FResultsPage

class MetodosAcopladosPage(QWidget):
    """
    A QWidget subclass representing the Metodos Acoplados page.

    This page currently displays three placeholder LaTeX equations and
    includes a 'Back' button to return to the previous page and a 'Graphics'
    button intended for showing graphics (placeholder functionality).
    """
    def __init__(self, parent, stack, n_eff_TE, n_eff_TM, lambd):
        """
        Initializes the MetodosAcopladosPage.

        Args:
            parent (QWidget): The parent widget.
            stack (QStackedWidget): The widget stack used for page navigation.
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
        # Create the main vertical layout
        layout = QVBoxLayout(self)
        
        # Title label for the page
        title = QLabel("Metodos Acoplados")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Create and add three placeholder LaTeX equations using LatexLabel
        # You can replace these placeholders with the actual LaTeX expressions later.
        equation1 = LatexLabel(r"$x$", fontsize=14)
        equation2 = LatexLabel(r"$y$", fontsize=14)
        equation3 = LatexLabel(r"$z$", fontsize=14)
        
        layout.addWidget(equation1, alignment=Qt.AlignCenter)
        layout.addWidget(equation2, alignment=Qt.AlignCenter)
        layout.addWidget(equation3, alignment=Qt.AlignCenter)
        
        # Create a horizontal layout for the buttons at the bottom
        buttons_layout = QHBoxLayout()
        
        # Back button: returns to the previous page
        back_btn = QPushButton("Back")
        back_btn.setFixedWidth(100)
        back_btn.clicked.connect(self.go_back)
        buttons_layout.addWidget(back_btn)
        
        # Graphics button: placeholder for graphics functionality
        graphics_btn = QPushButton("Graphics")
        graphics_btn.setFixedWidth(100)
        graphics_btn.clicked.connect(self.show_graphics)
        buttons_layout.addWidget(graphics_btn)
        
        # Add the buttons layout to the main layout
        layout.addLayout(buttons_layout)
        
        # Set the layout for this widget
        self.setLayout(layout)

    def go_back(self):
        """
        Navigates back to the previous page in the stack.
        """
        # Remove this page from the stack to go back to the previous page
        self.stack.removeWidget(self)

    def show_graphics(self):
        f_results_page = FResultsPage(self, self.stack, self.n_eff_TE, self.n_eff_TM, self.lambd)

        # Add the new page to the stack.
        self.stack.addWidget(f_results_page)
        
        # Set the current widget in the stack to the new Metodos Acoplados page.
        self.stack.setCurrentWidget(f_results_page)
