from ...helpers import Int, Json, Schema, Str


class SessionKey(Schema):
    session_key = Str()
    unionid = Str()
    openid = Str()
    raw_data = Json()


class UserMixin:
    def get_session_key(self, js_code):
        """(小程序)文档见https://developers.weixin.qq.com/miniprogram
        /dev/api-backend/open-api/login/auth.code2Session.html
        -------
        请求参数
        属性    类型    默认值  必填    说明
        appid   string      是  小程序 appId
        secret  string      是  小程序 appSecret
        js_code     string      是  登录时获取的 code
        grant_type  string      是  授权类型，此处只需填写 authorization_code
        -------
        正常响应
        openid   string  用户唯一标识
        session_key     string  会话密钥
        unionid     string  用户在开放平台的唯一标识符，在满足 UnionID
        下发条件的情况下会返回，详见 UnionID 机制说明。
        errcode     number  错误码
        errmsg  string  错误信息
        ----
        异常响应
        值  说明    最低版本
        -1  系统繁忙，此时请开发者稍候再试
        0   请求成功
        40029   code 无效
        45011   频率限制，每个用户每分钟100次
        """
        params = {
            'appid': self.auth.appid,
            'secret': self.auth.secret,
            'js_code': js_code,
            'grant_type': 'authorization_code'
        }
        with self._do_request('GET', 'sns/jscode2session',
                              params=params) as resp_json:
            # 注意: unionid可能为None, 使用前需要判断
            return SessionKey(session_key=resp_json['session_key'],
                              unionid=resp_json.get('unionid'),
                              openid=resp_json['openid'],
                              raw_data=resp_json)
