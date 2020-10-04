import time


class Auth:
    def __init__(self, appid, secret, cache, callback_token=None):
        self.appid = appid
        self.secret = secret
        self.cache = cache
        self.callback_token = callback_token

    @property
    def access_token(self):
        return self.cache.get_access_token(self.appid)

    def update_access_token(self, value, create_time, expires_in):
        return self.cache.update_access_token(
            self.appid,
            value,
            create_time,
            expires_in,
        )

    @access_token.setter
    def access_token(self, value):
        self.update_access_token(value, time.time(), expires_in=5400)

    @property
    def js_ticket(self):
        return self.cache.get_js_ticket(self.appid)

    def update_js_ticket(self, value, create_time, expires_in):
        return self.cache.update_js_ticket(
            self.appid,
            value,
            create_time,
            expires_in,
        )

    @js_ticket.setter
    def js_ticket(self, value):
        return self.update_js_ticket(value, time.time(), expires_in=5400)
