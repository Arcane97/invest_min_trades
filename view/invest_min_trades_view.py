import logging
from PyQt5.QtWidgets import QMainWindow

from view.invest_min_trades_view_ui import Ui_MainWindow
from utils.text_editor_logger import QTextEditLogger


class InvestMinTradesView(QMainWindow):
    def __init__(self, controller, model, log_name="invest_min_trades"):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._controller = controller
        self._model = model

        self._logger = logging.getLogger(f'{log_name}.view')
        self._create_log(log_name)

        self._connect_signals()

    def _create_log(self, log_name):
        main_logger = logging.getLogger(log_name)
        # обработчик окна логов
        log_window_handler = QTextEditLogger(self.ui.log_tedit)
        formatter_wh = logging.Formatter('%(asctime)s -split- %(levelname)s -split- %(message)s')
        log_window_handler.setFormatter(formatter_wh)
        # добавление обработчиков к логгеру
        main_logger.addHandler(log_window_handler)

    def _connect_signals(self):
        self.ui.working_btn.clicked.connect(self._working_btn_clicked)

    def _working_btn_clicked(self):
        if self._model.is_working:
            self._controller.stop_thread()
            self.ui.working_btn.setText('Старт')
        else:
            self._controller.start_thread()
            self.ui.working_btn.setText('Стоп')

    def load_params(self, pair, num_trades):
        try:
            self.ui.pair_ledit.setText(pair)
        except:
            self._logger.exception('При загрузке пары в интерфейс произошла ошибка')

        try:
            self.ui.num_trades_ledit.setText(str(num_trades))
        except:
            self._logger.exception('При загрузке количества трейдов в интерфейс произошла ошибка')

    def closeEvent(self, e):
        self._controller.save_params()
        self._controller.terminate_threads()
