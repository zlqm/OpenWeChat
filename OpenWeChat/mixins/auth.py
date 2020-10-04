from collections import namedtuple
import time
from ..helpers import Int, Json, Str, Schema


class Token(Schema):
    value = Str()
    expires_in = Int()
    raw_data = Json()


class CredentialsMixin:
    def get_new_access_token(self):
        """向微信服务器申请新的access_token
        注:
          1. 因为存在接口调用上限， token 应由 **指定的服务** 进行维护更新, 不要随意调用
          2. 本接口需要将调用主机的 IP 加入到公众号的 IP 白名单中

        (服务端)文档见https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140183
        正常情况下，微信会返回下述JSON数据包给公众号：
        {"access_token":"ACCESS_TOKEN","expires_in":7200}
        """
        params = {
            'grant_type': 'client_credential',
            'appid': self.auth.appid,
            'secret': self.auth.secret
        }
        with self._do_request('GET', '/cgi-bin/token',
                              params=params) as resp_json:
            data = Token(value=resp_json['access_token'],
                         expires_in=resp_json['expires_in'],
                         raw_data=resp_json)
            self.logger.info(
                '[new_token: %s] [expires_in: %s] '
                '[hint: get_new_access_token]', data.value, data.expires_in)
            return data

    def refresh_access_token(self):
        """重新获取access_token并刷新缓存，由 **指定服务**维护，不要随意调用!!
        """
        create_time = int(time.time())
        data = self.get_new_access_token()
        return self.auth.update_access_token(data.value, create_time,
                                                data.expires_in)

    def get_new_js_ticket(self):
        """向微信服务器申请新的js_ticket
        注: ticket应由 **指定的服务** 进行维护更新
        (服务端)文档见https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421141115
        附录1-JS-SDK使用权限签名算法
        成功返回如下JSON：

        {
            "errcode":0,
            "errmsg":"ok",
            "ticket":"ticket",
            "expires_in":7200
        }
        """
        params = {
            'access_token': self.auth.access_token,
            'type': 'jsapi'
        }
        with self._do_request('GET',
                              '/cgi-bin/ticket/getticket',
                              params=params) as resp_json:
            data = Token(
                value=resp_json['ticket'],
                expires_in=resp_json['expires_in'],
                raw_data=resp_json,
            )
            self.logger.info(
                '[new_token: %s] [expires_in: %s] hint: get_new_js_ticket',
                data.value, data.expires_in)
            return data

    def refresh_js_ticket(self, *args, **kwargs):
        """重新获取js_ticket并刷新缓存，由 **指定服务** 维护，不要随意调用!!
        """
        create_time = int(time.time())
        data = self.get_new_js_ticket()
        return self.auth.update_js_ticket(
            data.value,
            create_time,
            data.expires_in,
        )
