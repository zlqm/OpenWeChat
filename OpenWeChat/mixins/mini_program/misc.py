import base64
import json

from Crypto.Cipher import AES


class InvalidEncryptedData(ValueError):
    pass


def _unpad(s):
    return s[:-ord(s[len(s) - 1:])]


def decrypt_data(encrypted_data, iv, session_key, appid):
    """(小程序)文档见https://developers.weixin.qq.com/miniprogram
    /dev/framework/open-ability/signature.html
    :params data: 包括敏感数据在内的完整用户信息的加密数据
    :params iv: 加密算法的初始向量
    :params session_key: 会话密钥, 是对用户数据进行 加密签名 的密钥
    """
    session_key = base64.b64decode(session_key)
    encrypted_data = base64.b64decode(encrypted_data)
    iv = base64.b64decode(iv)
    cipher = AES.new(session_key, AES.MODE_CBC, iv)
    text = _unpad(cipher.decrypt(encrypted_data))
    decrypted = json.loads(text, encoding='utf8')
    if decrypted['watermark']['appid'] != appid:
        raise InvalidEncryptedData('appid {} does not match {}'.format(
            decrypted['watermark']['appid'], appid))
    return decrypted


class MiscMixin:
    def decrypt_data(self, encrypted_data, iv, session_key):
        """(小程序)文档见https://developers.weixin.qq.com/miniprogram
        /dev/framework/open-ability/signature.html
        :params data: 包括敏感数据在内的完整用户信息的加密数据
        :params iv: 加密算法的初始向量
        :params session_key: 会话密钥, 是对用户数据进行 加密签名 的密钥
        """

        return decrypt_data(encrypted_data, iv, session_key, self.auth.appid)
