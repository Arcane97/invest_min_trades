import logging
import os
from PyQt5.QtWidgets import QMainWindow, QAction, QMessageBox

from view.api_saver.api_saver_gui import APISaverGUI
from view.invest_min_trades_view_ui import Ui_MainWindow
from utils.constants import LOG_FILE_NAME
from utils.singleton import InvestMinTradesSingleton
from utils.text_editor_logger import QTextEditLogger


class InvestMinTradesView(QMainWindow):
    def __init__(self, controller, model, log_name="invest_min_trades"):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._controller = controller
        self._model = model

        self._singleton = InvestMinTradesSingleton()

        self._create_menubar()

        self._logger = logging.getLogger(f'{log_name}.view')
        self._create_log(log_name)

        self._connect_signals()

    def _create_menubar(self):
        """ Создание менюбара (сверху окна)
        """
        # кнопка открытия файла логов
        open_log_file_act = QAction('Открыть файл логов', self)
        open_log_file_act.triggered.connect(self._open_log_file)
        # кнопка очиститки файла логов
        clear_log_file_act = QAction('Очистить файл логов', self)
        clear_log_file_act.triggered.connect(self._clear_log_file)
        # кнопка сброса API ключа в меню баре
        open_api_saver_act = QAction('Сбросить API ключ и сохранить новый', self)
        open_api_saver_act.triggered.connect(self._open_api_saver_win)

        # заполнение меню бара
        menubar = self.menuBar()
        log_menu = menubar.addMenu('Лог')
        log_menu.addAction(open_log_file_act)
        log_menu.addAction(clear_log_file_act)
        api_menu = menubar.addMenu('API')
        api_menu.addAction(open_api_saver_act)

    def _open_log_file(self):
        """ Открытие файла логов (в винде)
        """
        try:
            os.startfile(LOG_FILE_NAME)
        except Exception:
            self._logger.exception('Не удалось открыть файл логов')

    def _clear_log_file(self):
        """ Очиститка файла логов
        """
        msg = QMessageBox(self)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setWindowTitle('Лог')
        msg.setText('Очистить файл логов?')
        msg.exec_()
        if msg.result() == QMessageBox.Yes:
            with open(LOG_FILE_NAME, "w") as out:
                out.write('')
                self.statusBar().showMessage('Файл логов очищен')
        else:
            self.statusBar().showMessage('Отмена очистки файла логов')

    def _open_api_saver_win(self):
        """ Вызов онка сохранения API ключей
        """
        api_saver_win = APISaverGUI(self._model, parent=self)
        api_saver_win.setModal(True)
        api_saver_win.show()
        self.statusBar().showMessage('Вызов окна сохранения API ключей')

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
        if self._singleton.is_working:
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
