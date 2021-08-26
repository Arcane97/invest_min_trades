import logging

from view.invest_min_trades_view import InvestMinTradesView


class InvestMinTradesController:
    def __init__(self, model, log_name="invest_min_trades"):
        self._model = model

        self._logger = logging.getLogger(f'{log_name}.controller')

        self._view = InvestMinTradesView()

        self._view.show()
