from contextlib import contextmanager
import json

import requests
from requests.compat import json as complexjson

from . import exceptions


class Session:
    def __init__(self, *, pool_size=10, timeout=10, logger=None):
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter
        self.session.mount(
            'http://',
            adapter(pool_connections=pool_size, pool_maxsize=pool_size))
        self.session.mount(
            'https://',
            adapter(pool_connections=pool_size, pool_maxsize=pool_size))
        self.timeout = timeout
        self.logger = logger

    @contextmanager
    def do_request(self,
                   method,
                   url,
                   timeout=None,
                   json_ensure_ascii=False,
                   resp_encoding='utf8',
                   **kwargs):
        default_kwargs = {
            'timeout': timeout or self.timeout,
        }
        if not kwargs.get('data') and kwargs.get('json'):
            data = json.dumps(kwargs['json'], ensure_ascii=json_ensure_ascii)
            headers = kwargs.get('headers', {})
            headers['Content-Type'] = 'application/json; charset=utf-8'
            kwargs['data'] = data.encode('utf8')
            kwargs['headers'] = headers
        kwargs.update(**default_kwargs)
        info = [
            'do_request',
            'method: {}'.format(method),
            'url: {}'.format(url),
        ]
        try:
            resp = self.session.request(method.upper(), url, **kwargs)
            resp.encoding = 'utf8'
            resp_json = resp.json()
            info.append('error_code: {}'.format(resp_json.get('errcode')))
            if 'errcode' in resp_json and resp_json['errcode'] != 0:
                error_code = int(resp_json['errcode'])
                hint = resp_json.get('errmsg', '')
                api_error = exceptions.make_api_error(error_code,
                                                      resp.status_code,
                                                      resp.content,
                                                      hint=hint)
                info.append('content: {}'.format(resp.content))
                self.logger and self.logger.error(' '.join(info))
                raise api_error
            try:
                yield resp_json
            except KeyError as err:
                info.append('hint: KeyError')
                self.logger and self.logger.error(' '.join(info))
                raise exceptions.InvalidResponse(err)
        except requests.exceptions.Timeout as err:
            info.append('hint: timeout. err: {}'.format(err))
            self.logger and self.logger.error(' '.join(info))
            raise exceptions.Timeout(err)
        except requests.HTTPError as err:
            info.append('hint: HTTPError. err: {}'.format(err))
            self.logger and self.logger.error(' '.join(info))
            raise exceptions.NetworkError(err)
        except complexjson.JSONDecodeError as err:
            info.append('hint: JSONDecodeError. err: {}'.format(err))
            self.logger and self.logger.error(' '.join(info))
            raise exceptions.InvalidResponse(err)
        except Exception as err:
            info.append('hint: unexpected err. err: {}'.format(err))
            self.logger and self.logger.error(' '.join(info))
            raise exceptions.SDKError(err)
