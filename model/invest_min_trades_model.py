import logging
from PyQt5.QtCore import QObject

from model.yobit_private_api import YobitPrivateAPI
from model.yobit_public_api import YobitPublicAPI


class InvestMinTradesModel(QObject):
    def __init__(self, api_key, api_secret, pair, num_trades, log_name="invest_min_trades"):
        super().__init__()
        self.api_key = api_key
        self.api_secret = api_secret
        self.pair = pair
        self.num_trades = num_trades

        self.is_working = False
        self._min_amount = 0.0001

        self._yobit_private_api_obj = YobitPrivateAPI(api_key, api_secret.encode(), self.pair, log_name=log_name)
        self._yobit_public_api_obj = YobitPublicAPI(self.pair)

        self._logger = logging.getLogger(f'{log_name}.model')

    def set_api_key(self, api_key):
        self.api_key = api_key
        self._yobit_private_api_obj.api_key = self.api_key

    def set_api_secret(self, api_secret):
        self.api_secret = api_secret.encode()
        self._yobit_private_api_obj.api_secret = self.api_secret

    def set_pair(self, pair):
        self.pair = pair
        self._yobit_private_api_obj.pair = self.pair
        self._yobit_public_api_obj = self.pair

    def start_trades(self):
        self._logger.info('Старт')
        self.is_working = True
        last_trade = self._get_last_trade()
        while self.is_working and self.num_trades > 0:
            price, quantity = self._get_price_and_quantity()
            result = self._do_trade(price, quantity)

            if isinstance(result, str):
                last_trade = self._get_last_trade()
                self.num_trades -= 1
                self._logger.info(f'Трейд успешно выполнен. Осталось тредов: {self.num_trades}')
            else:
                self._logger.info('При трейде вознилка ошибка, проверяем исполнился ли ордер')
                if self._check_trade(last_trade):
                    last_trade = self._get_last_trade()
                    self.num_trades -= 1
                    self._logger.info(f'Трейд успешно выполнен. Осталось тредов: {self.num_trades}')
                else:
                    self._logger.info('Трейд не выполнен, пытаемя снова')

    def stop_trades(self):
        self._logger.info('Стоп')
        self.is_working = False

    def _get_price_and_quantity(self):
        glass = self._yobit_public_api_obj.get_yobit_glass()
        amount = 0.0
        quantity = 0.0
        glass_index = 0
        while amount < self._min_amount:
            price, glass_quantity = glass[glass_index]
            amount = price * glass_quantity
            glass_index += 1

        if glass_index == 1:
            quantity = round(self._min_amount / price, 8)
            return price, quantity

        for index in range(glass_index-1):
            quantity += glass[index][1]

        quantity += round(self._min_amount / price, 8)
        return price, quantity

    def _do_trade(self, price, quantity):
        return self._yobit_private_api_obj.place_order_buy(price, quantity)

    def _check_trade(self, last_trade):
        trade_history = self._yobit_private_api_obj.get_trade_history()
        new_trade = next(iter(trade_history))

        return new_trade != last_trade

    def _get_last_trade(self):
        trade_history = self._yobit_private_api_obj.get_trade_history()
        return next(iter(trade_history))


if __name__ == "__main__":
    model = InvestMinTradesModel("", "", "rur_usdt", 3)
    result = model._get_price_and_quantity()
    print('result', result, result[0]*result[1])
    #
    # order_id = model._do_trade(*result)
    # print(order_id)
