import json
import logging
import os
from PyQt5 import QtWidgets, QtCore

from view.api_saver.api_saver_gui_ui import Ui_API_keys_saver
from utils.api_key_encryption import encrypt
from utils.constants import SETTINGS_FILE_NAME


class APISaverGUI(QtWidgets.QDialog):
    """ Окно сохранения API ключей
    """

    def __init__(self, model, next_win=None, parent=None, log_name="invest_min_trades"):
        super().__init__(parent)

        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self._model = model

        # следующее окно, которое откроестся после закрытия жанного окна
        self.next_win = next_win

        self.ui = Ui_API_keys_saver()
        self.ui.setupUi(self)

        self._logger = logging.getLogger(f'{log_name}.api_saver')

        self.ui.api_save_btn.clicked.connect(self.save_api_key)

    def _set_to_model(self, api_key, api_secret):
        if self._model is not None:
            self._model.set_api_key(api_key)
            self._model.set_api_secret(api_secret)

    @staticmethod
    def _create_settings_file():
        with open(SETTINGS_FILE_NAME, "w") as file:
            data = {
                'api_key': '',
                'api_secret': '',
                'pair': 'yo_btc',
                'num_trades': 10,
            }

            json.dump(data, file)

    def _save_to_file(self, api_key, api_secret):
        with open(SETTINGS_FILE_NAME, "r") as file:
            settings_data = json.load(file)
            if not isinstance(settings_data, dict):
                # error кривой json файл
                self._logger.error(f'Кривой файл настроек. Удалите его: {SETTINGS_FILE_NAME}')

        with open(SETTINGS_FILE_NAME, "w") as file:
            encrypted_api_key = encrypt(api_key)
            encrypted_api_secret = encrypt(api_secret)
            settings_data['api_key'] = encrypted_api_key
            settings_data['api_secret'] = encrypted_api_secret
            json.dump(settings_data, file)
            self._logger.info('API ключи сохранены')

    def save_api_key(self):
        api_key = self.ui.api_key_ledit.text()
        api_secret = self.ui.api_secret_ledit.text()

        if len(api_key) == 0:
            QtWidgets.QMessageBox.about(self, 'Предупреждение', 'Введите API ключ!')
            return
        if len(api_secret) == 0:
            QtWidgets.QMessageBox.about(self, 'Предупреждение', 'Введите API secret!')
            return

        if not os.path.exists(SETTINGS_FILE_NAME):
            self._create_settings_file()

        self._save_to_file(api_key, api_secret)
        self._set_to_model(api_key, api_secret)

        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle('Сохранение')
        msg.setText("API ключи сохранены")

        if msg.exec_():
            if self.next_win is not None:
                self.next_win.show()
            self.close()
