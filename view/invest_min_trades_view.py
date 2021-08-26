from PyQt5.QtWidgets import QMainWindow

from view.invest_min_trades_view_ui import Ui_MainWindow


class InvestMinTradesView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
