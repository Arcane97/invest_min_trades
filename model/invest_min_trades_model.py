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

        self._min_amount = 0.0001

        self._yobit_private_api_obj = YobitPrivateAPI(api_key, api_secret.encode(), self.pair, log_name=log_name)
        self._yobit_public_api_obj = YobitPublicAPI(self.pair)

        self._logger = logging.getLogger(f'{log_name}.model')

    def set_pair(self, pair):
        self.pair = pair
        self._yobit_private_api_obj.pair = self.pair
        self._yobit_public_api_obj = self.pair

    def _get_price_and_quantity(self):
        glass = self._yobit_public_api_obj.get_yobit_glass()
        amount = 0.0
        quantity = 0.0
        glass_index = 0
        while amount < self._min_amount:
            price, glass_quantity = glass[glass_index]
            print(price, glass_quantity)
            amount = price * glass_quantity
            glass_index += 1

        if glass_index == 1:
            quantity = round(self._min_amount / price, 8)
            return price, quantity

        for index in range(glass_index-1):
            quantity += glass[index][1]

        quantity += round(self._min_amount / price, 8)
        return price, quantity


if __name__ == "__main__":
    model = InvestMinTradesModel("", "", "rur_usdt", 1)
    result = model._get_price_and_quantity()
    print('result', result, result[0]*result[1])
