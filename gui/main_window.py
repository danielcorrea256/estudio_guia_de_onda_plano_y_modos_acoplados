import sys
from PySide6.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout
from gui.home_page import HomePage
from gui.form_page import FormPage
from gui.results_page import ResultsPage

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-View Application")
        self.setMinimumSize(1200, 800)

        self.stack = QStackedWidget()

        self.home_page = HomePage()
        self.form_page = FormPage()
        self.results_page = ResultsPage()

        self.stack.addWidget(self.home_page)    # index 0
        self.stack.addWidget(self.form_page)    # index 1
        self.stack.addWidget(self.results_page) # index 2

        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)

        # Connect the buttons to navigate
        self.home_page.go_to_form_btn.clicked.connect(self.show_form)
        self.form_page.submit_btn.clicked.connect(self.show_results)

    def show_form(self):
        self.stack.setCurrentWidget(self.form_page)

    def show_results(self):
        """
        1. Gather data from the form.
        2. Pass data to the results page.
        3. Switch to the results page.
        """

        n_co = float(self.form_page.n_co_input.text())
        n_cl = float(self.form_page.n_cl_input.text())
        n_t = float(self.form_page.n_t_input.text())
        h = float(self.form_page.h_input.text())
        k_0 = float(self.form_page.k_0_input.text())
        lambd = float(self.form_page.lambda_input.text())

        # Pass the form data into the results page
        self.results_page.set_data(
            n_co=n_co, 
            n_cl=n_cl, 
            n_t=n_t,
            h=h,
            k_0=k_0,
            lambd=lambd
        )

        # Now switch to the results page
        self.stack.setCurrentWidget(self.results_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
