import logging
import time
from PyQt5.QtCore import QObject

from model.yobit_private_api import YobitPrivateAPI
from model.yobit_public_api import YobitPublicAPI
from utils.singleton import InvestMinTradesSingleton


class InvestMinTradesModel(QObject):
    def __init__(self, api_key, api_secret, pair, num_trades, log_name="invest_min_trades"):
        super().__init__()
        self.api_key = api_key
        self.api_secret = api_secret
        self.pair = pair
        self.num_trades = num_trades

        self._singleton = InvestMinTradesSingleton()
        self._min_amount = 0.0001

        self._yobit_private_api_obj = YobitPrivateAPI(api_key, api_secret.encode(), self.pair, log_name=log_name)
        self._yobit_public_api_obj = YobitPublicAPI(self.pair)

        self._logger = logging.getLogger(f'{log_name}.model')

    def set_api_key(self, api_key):
        self.api_key = api_key
        self._yobit_private_api_obj.api_key = self.api_key
        self._logger.info('api_key загружен в модель')

    def set_api_secret(self, api_secret):
        self.api_secret = api_secret.encode()
        self._yobit_private_api_obj.api_secret = self.api_secret
        self._logger.info('api_secret загружен в модель')

    def set_pair(self, pair):
        self.pair = pair
        self._yobit_private_api_obj.pair = self.pair
        self._yobit_public_api_obj.pair = self.pair

    def _get_glass(self, is_complete_trade, glass):
        if is_complete_trade:
            new_glass = self._yobit_public_api_obj.get_yobit_glass()
            if new_glass is None:
                return None

            while self._singleton.is_working and glass == new_glass:
                self._logger.error('Получили старый стакан, получаем новый')
                time.sleep(2)
                new_glass = self._yobit_public_api_obj.get_yobit_glass()
            return new_glass
        else:
            return self._yobit_public_api_obj.get_yobit_glass()

    def start_trades(self):
        self._logger.info('Старт')
        self._singleton.is_working = True
        last_trade = self._get_last_trade()
        is_complete_trade = False
        glass = None
        while self._singleton.is_working and self.num_trades > 0:
            glass = self._get_glass(is_complete_trade, glass)
            if glass is None:
                return

            price, quantity = self._get_price_and_quantity(glass)
            if price is None:
                return

            self._do_trade(price, quantity)
            print(last_trade)
            is_complete_trade, last_trade = self._check_trade(last_trade)
            if is_complete_trade:
                self.num_trades -= 1
                self._logger.info(f'Трейд успешно выполнен. Осталось тредов: {self.num_trades}')
            else:
                self._logger.info('Трейд не выполнен, пытаемя снова')

            time.sleep(3)

    def stop_trades(self):
        self._logger.info('Стоп')
        self._singleton.is_working = False

    def _get_price_and_quantity(self, glass):
        amount = 0.0
        quantity = 0.0
        glass_index = 0
        while amount < self._min_amount:
            price, glass_quantity = glass[glass_index]
            amount = price * glass_quantity
            glass_index += 1

        if glass_index == 1:
            quantity = round(self._min_amount / price, 8)
            while round(quantity, 8) * price < self._min_amount:
                quantity += 0.00000001
            return price, round(quantity, 8)

        for index in range(glass_index-1):
            quantity += glass[index][1]

        qty = round(self._min_amount / price, 8)
        while round(qty, 8) * price < self._min_amount:
            qty += 0.00000001
        quantity += qty

        return price, round(quantity, 8)

    def _do_trade(self, price, quantity):
        return self._yobit_private_api_obj.place_order_buy(price, quantity)

    def _check_trade(self, last_trade):
        trade_history = self._yobit_private_api_obj.get_trade_history()
        if trade_history is None:
            return None, None

        new_trade = None
        for key, deal in trade_history.items():
            amount = deal['rate'] * deal['amount']
            if amount >= 0.0001:
                new_trade = key
                break

        if new_trade is None:
            return False, new_trade
        return new_trade != last_trade, new_trade

    def _get_last_trade(self):
        trade_history = self._yobit_private_api_obj.get_trade_history()
        if trade_history is None:
            return None

        last_trade = None
        for key, deal in trade_history.items():
            amount = deal['rate'] * deal['amount']
            if amount >= 0.0001:
                last_trade = key
                break
        return last_trade


if __name__ == "__main__":
    model = InvestMinTradesModel("", "", "rur_usdt", 3)
    result = model._get_price_and_quantity()
    print('result', result, result[0]*result[1])
    #
    # order_id = model._do_trade(*result)
    # print(order_id)
