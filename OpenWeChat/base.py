from contextlib import contextmanager
from urllib.parse import urljoin
import re

from .http import Session
from .logging import create_logger


class Base:
    base_url = 'https://api.weixin.qq.com'
    _url_pattern = re.compile(r'https?://.+')
    APP_TYPE = None

    def __init__(self,
                 auth,
                 base_url=None,
                 session=None,
                 timeout=20,
                 logger=None,
                 debug=False):
        self._auth = auth
        self.base_url = base_url or self.base_url
        self.timeout = timeout
        self.debug = debug
        self.logger = logger or create_logger(self)
        self.session = session or Session(timeout=timeout, logger=self.logger)

    def __str__(self):
        return '<{}({})>'.format(self.APP_TYPE, self.auth.appid)

    @property
    def auth(self):
        return self._auth

    @property
    def name(self):
        return self.auth.appid

    @contextmanager
    def _do_request(self, method, url, **kwargs):
        if not self._url_pattern.match(url):
            url = urljoin(self.base_url, url)
        with self.session.do_request(method, url, **kwargs) as resp_json:
            yield resp_json
