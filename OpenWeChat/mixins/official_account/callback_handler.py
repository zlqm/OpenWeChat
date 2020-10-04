import hashlib
import warnings


class CallbackHandlerMixin:
    def validate_callback_api(self, nonce, timestamp, signature):
        lst = sorted([self.auth.callback_token, nonce, timestamp])
        sha1 = hashlib.sha1()
        for item in lst:
            sha1.update(item.encode('utf8'))
        hash_code = sha1.hexdigest()
        return hash_code == signature
