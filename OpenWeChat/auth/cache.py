import abc

from .. import exceptions
from ..compat import complex_json


class Cache(abc.ABC):
    @abc.abstractmethod
    def get_access_token(self, appid):
        pass

    @abc.abstractmethod
    def update_access_token(self, appid, value, expires_in):
        pass

    @abc.abstractmethod
    def get_js_ticket(self, appid):
        pass

    @abc.abstractmethod
    def update_js_ticket(self, appid, value, expires_in):
        pass


class DummyCache(Cache):
    def __init__(self, key_prefix='wechat'):
        self.key_prefix = key_prefix

    def get_credential_data(self, key):
        raise NotImplementedError

    def load_credential_data(self, raw_data):
        return complex_json.loads(raw_data)['value']

    def get_access_token(self, appid):
        key = '{}:token:{}'.format(self.key_prefix, appid)
        raw_data = self.get_credential_data(key)
        try:
            return self.load_credential_data(raw_data)
        except (KeyError, TypeError):
            raise exceptions.AccessTokenIsCorrupted(
                'invalid token cache: {}'.format(str(raw_data)))

    def get_js_ticket(self, appid):
        key = '{}:ticket:{}'.format(self.key_prefix, appid)
        raw_data = self.get_credential_data(key)
        try:
            return self.load_credential_data(raw_data)
        except (KeyError, TypeError):
            raise exceptions.JSTicketIsCorrupted(
                'invalid ticket cache: {}'.format(str(raw_data)))

    def update_credential_data(self, key, value, expires_in):
        raise NotImplementedError

    def dump_credential_data(self, value, create_time, expires_in):
        data = {
            'value': value,
            'create_time': create_time,
            'expires_in': expires_in,
        }
        return complex_json.dumps(data)

    def update_access_token(self, appid, value, create_time, expires_in):
        key = '{}:token:{}'.format(self.key_prefix, appid)
        value = self.dump_credential_data(value, create_time, expires_in)
        return self.update_credential_data(key, value, expires_in)

    def update_js_ticket(self, appid, value, create_time, expires_in):
        key = '{}:ticket:{}'.format(self.key_prefix, appid)
        value = self.dump_credential_data(value, create_time, expires_in)
        return self.update_credential_data(key, value, expires_in)


class RedisCache(DummyCache):
    def __init__(self, redis_client, **kwargs):
        self.redis_client = redis_client
        super().__init__(**kwargs)

    def get_credential_data(self, key):
        return self.redis_client.get(key)

    def update_credential_data(self, key, value, expires_in):
        return self.redis_client.set(key, value, ex=expires_in)
