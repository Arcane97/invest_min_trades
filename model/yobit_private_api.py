import hashlib
import hmac
import http.client
import json
import os
import urllib
import base64
import logging

from utils.constants import NONCE_FILE_NAME, DEFAULT_TIMEOUT


# Будем перехватывать все сообщения об ошибках с биржи
class YobitException(Exception):
    pass


class YobitBAN(Exception):
    pass


class YobitNotAvailable(Exception):
    pass


class ProxyException(Exception):
    pass


class YobitPrivateAPI:
    def __init__(self, api_key, api_secret, proxies=None, time_out=DEFAULT_TIMEOUT, log_name="yobit_private_api"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.time_out = time_out
        self.proxies = proxies

        self._logger = logging.getLogger(f'{log_name}.yobit_private_api')

    def _get_nonce(self):
        # Каждый новый запрос к серверу должен содержать увеличенное число в диапазоне 1-2147483646
        # Поэтому храним число в файле поблизости, каждый раз обновляя его
        if not os.path.exists(NONCE_FILE_NAME):
            with open(NONCE_FILE_NAME, "w") as out:
                out.write('1')
                self._logger.info('nonce файл создан')

        # При каждом обращении к торговому API увеличиваем счетчик nonce на единицу
        with open(NONCE_FILE_NAME, 'r+') as inp:
            nonce = int(inp.read())
            inp.seek(0)
            inp.write(str(nonce + 1))
            inp.truncate()

        return nonce

    def _call_api(self, **kwargs):
        nonce = self._get_nonce()
        if nonce >= 2147483646:
            self._logger.critical('Обновите API ключ, число nonce достигло ' + str(nonce))
            raise YobitException('Обновите API ключ, число nonce достигло ' + str(nonce))

        try:
            payload = {'nonce': nonce}

            if kwargs:
                payload.update(kwargs)
            payload = urllib.parse.urlencode(payload)

            hash_obj = hmac.new(key=self.api_secret, digestmod=hashlib.sha512)
            hash_obj.update(payload.encode('utf-8'))
            sign = hash_obj.hexdigest()

            headers = {"Content-type": "application/x-www-form-urlencoded",
                       "Key": self.api_key,
                       "Sign": sign}

            # подключение прокси
            if self.proxies is None:
                conn = http.client.HTTPSConnection("yobit.net", timeout=self.time_out)
            else:
                try:
                    proxies_url = urllib.parse.urlparse(self.proxies)
                    proxies_host = proxies_url.hostname
                    proxies_port = int(self.proxies[self.proxies.rfind(':')+1:])
                    conn = http.client.HTTPSConnection(host=proxies_host, port=proxies_port, timeout=self.time_out)

                    proxies_headers = {}
                    auth = '%s:%s' % (proxies_url.username, proxies_url.password)
                    encode_auth = base64.b64encode(auth.encode()).decode()
                    proxies_headers['Proxy-Authorization'] = 'Basic ' + encode_auth
                    conn.set_tunnel('yobit.net', headers=proxies_headers)
                except Exception as e:
                    raise ProxyException('ProxyException: ' + str(e))  # todo добавить обработку

            conn.request("POST", "/tapi/", payload, headers)
            response_obj = conn.getresponse()

            response = response_obj.read()
            if response == b'error code: 1015':
                raise YobitBAN('Получили бан!')

            conn.close()

        except YobitBAN as ban:
            self._logger.error('Получили бан!')
            raise YobitBAN('Получили бан!')
        except Exception as e:
            self._logger.critical('Ошибка полдключения по API ключу')
            raise YobitException('Ошибка полдключения по API ключу', e)

        try:
            obj = json.loads(response.decode('utf-8'))

            if 'error' in obj and obj['error']:
                self._logger.critical('Yobit выдал ошибку: ' + str(obj['error']))
                raise YobitException(obj['error'])
            return obj
        except json.decoder.JSONDecodeError:
            self._logger.critical('Ошибка анализа возвращаемых данных, получена строка' + str(response))
            raise YobitException('Ошибка анализа возвращаемых данных, получена строка', response)


if __name__ == '__main__':
    api_key = ""
    api_secret = b""
    api_obj = YobitPrivateAPI(api_key, api_secret)
    info = api_obj._call_api(method="getInfo")
    print(info)
