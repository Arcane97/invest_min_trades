import logging
import requests
from requests.packages.urllib3.util.retry import Retry

from utils.singleton import InvestMinTradesSingleton
from utils.timeout_http_adapter import TimeoutHTTPAdapter

YOBIT_DEPTH_LINK = "https://www.yobit.net/api/3/depth/"


class YobitPublicAPI:
    def __init__(self, pair, log_name="invest_min_trades"):
        self.pair = pair

        self.proxies = None

        self._logger = logging.getLogger(f'{log_name}.yobit_public_api')
        self._singleton = InvestMinTradesSingleton()

    def _make_request(self, url):
        try:
            s = requests.Session()
            retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504],
                            method_whitelist=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"])
            s.mount('http://', TimeoutHTTPAdapter(max_retries=retries))
            s.mount('https://', TimeoutHTTPAdapter(max_retries=retries))

            glass_req = s.get(url, proxies=self.proxies)
        except:
            self._logger.exception('Ошибка при получении данных из стакана')
            return None

        return glass_req

    def get_yobit_glass(self):
        """ Получение стакана yobit
        :return: стакан
        """
        is_complete = False
        glass = None
        while not is_complete and self._singleton.is_working:
            self._logger.info('Попытка получить стакан yobit')
            # получаем стакан с ордерами на покупку
            query = YOBIT_DEPTH_LINK + self.pair + '?limit=10'
            glass_req = self._make_request(query)

            if glass_req is None:
                continue

            # попытка расшифровать json файл
            try:
                glass_req_result = glass_req.json()
                glass = glass_req_result[self.pair]['asks']
                is_complete = True
            except Exception as e:
                self._logger.error('Ошибка в попытке расшифровать json файл')
                self._logger.error(e)
                is_complete = False

        self._logger.info(f'Получили стакан {glass}')
        return glass


if __name__ == "__main__":
    api_obj = YobitPublicAPI("rur_usdt")
    glass_ = api_obj.get_yobit_glass()
    print(glass_)
