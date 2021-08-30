import logging
import os

from view.invest_min_trades_view import InvestMinTradesView
from view.api_saver.api_saver_gui import APISaverGUI
from utils.constants import SETTINGS_FILE_NAME


class InvestMinTradesController:
    def __init__(self, model, log_name="invest_min_trades"):
        self._model = model

        self._logger = logging.getLogger(f'{log_name}.controller')

        self._view = InvestMinTradesView()

        if not os.path.exists(SETTINGS_FILE_NAME):
            self._api_saver = APISaverGUI(self._view, log_name="invest_min_trades")
            self._api_saver.show()
        else:
            self._view.show()

    def set_api_key(self):
        pass

    def set_api_secret(self):
        pass

    def set_pair(self):
        pass

    def set_num_trades(self):
        pass
