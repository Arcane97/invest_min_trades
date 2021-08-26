import logging
import sys

from PyQt5.QtWidgets import QApplication

from controller.invest_min_trades_controller import InvestMinTradesController
from model.invest_min_trades_model import InvestMinTradesModel
from utils.constants import LOG_FILE_NAME


def create_log(log_name):
    # логгер
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.INFO)
    # обработчик файла логов
    file_handler = logging.FileHandler(LOG_FILE_NAME)
    # форматирование файла логов
    formatter_fh = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter_fh)
    # добавление обработчиков к логгеру
    logger.addHandler(file_handler)


def main():
    log_name = "invest_min_trades"
    create_log(log_name)
    app = QApplication(sys.argv)

    model = InvestMinTradesModel("", "", "rur_usdt", 1, log_name)

    controller = InvestMinTradesController(model, log_name)

    app.exec()


sys.exit(main())
