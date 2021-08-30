import logging
from PyQt5.QtWidgets import QMainWindow

from view.invest_min_trades_view_ui import Ui_MainWindow


class InvestMinTradesView(QMainWindow):
    def __init__(self, controller, model, log_name="invest_min_trades"):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._controller = controller
        self._model = model

        self._logger = logging.getLogger(f'{log_name}.view')

    def load_params(self, pair, num_trades):
        try:
            self.ui.pair_ledit.setText(pair)
        except:
            self._logger.exception('При загрузке пары в интерфейс произошла ошибка')

        try:
            self.ui.num_trades_ledit.setText(str(num_trades))
        except:
            self._logger.exception('При загрузке количества трейдов в интерфейс произошла ошибка')
