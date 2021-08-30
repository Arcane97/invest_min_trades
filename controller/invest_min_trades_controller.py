import json
import logging
import os

from view.invest_min_trades_view import InvestMinTradesView
from view.api_saver.api_saver_gui import APISaverGUI
from utils.constants import SETTINGS_FILE_NAME
from utils.api_key_encryption import decrypt


class InvestMinTradesController:
    def __init__(self, model, log_name="invest_min_trades"):
        self._model = model

        self._logger = logging.getLogger(f'{log_name}.controller')

        self._view = InvestMinTradesView(self, self._model, log_name)

        if not os.path.exists(SETTINGS_FILE_NAME):
            self._api_saver = APISaverGUI(self._model, next_win=self._view, log_name="invest_min_trades")
            self._api_saver.show()
        else:
            self._view.show()
            self._load_params()

    def _load_params(self):
        if not os.path.exists(SETTINGS_FILE_NAME):
            with open(SETTINGS_FILE_NAME, "w") as file:
                data = {
                    'api_key': '',
                    'api_secret': '',
                    'pair': 'yo_btc',
                    'num_trades': 10,
                }

                json.dump(data, file)

        with open(SETTINGS_FILE_NAME, "r") as file:
            settings_data = json.load(file)
            if isinstance(settings_data, dict):
                api_key = settings_data.get('api_key')
                api_secret = settings_data.get('api_secret')
                pair = settings_data.get('pair')
                num_trades = settings_data.get('num_trades')
                self.set_api_keys(api_key, api_secret)
                self._view.load_params(pair, num_trades)
                self._set_param_model()
            else:
                # error кривой json файл
                self._logger.error(f'Кривой файл настроек. Удалите его: {SETTINGS_FILE_NAME}')
                self._view.load_params('yo_btc', 1.0)
                self._set_param_model()

    def set_api_keys(self, api_key, api_secret):
        decrypt_api_key = decrypt(api_key)
        decrypt_api_secret = decrypt(api_secret)
        self._model.set_api_key(decrypt_api_key)
        self._model.set_api_secret(decrypt_api_secret)

    def set_pair(self):
        try:
            pair = self._view.ui.pair_ledit.text()
            self._model.set_pair(pair)
        except Exception:
            self._logger.exception('Ошибка при попытке считать пару')
        else:
            self._logger.info(f'В программу введена пара: {pair}')

    def set_num_trades(self):
        try:
            num_trades = self._view.ui.num_trades_ledit.text()
            self._model.num_trades = num_trades
        except Exception:
            self._logger.exception('Ошибка при попытке считать количество трейдов')
        else:
            self._logger.info(f'В программу введено количество трейдов: {num_trades}')

    def _set_param_model(self):
        self.set_pair()
        self.set_num_trades()
