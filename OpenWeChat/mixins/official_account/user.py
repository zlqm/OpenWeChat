from ...helpers import Int, Json, Schema, Str


class OAuthToken(Schema):
    token = Str()
    openid = Str()
    raw_data = Json()


class UserInfo(Schema):
    openid = Str()
    unionid = Str()
    nickname = Str()
    avatar_url = Str()
    raw_data = Json()


class UserMixin:
    def get_oauth_token(self, oauth_code):
        """网页开发授权使用的token
        (公众号)文档见: https://mp.weixin.qq.com/wiki?t=resource/
        res_main&id=mp1421140842
        ---------
        正确时返回的JSON数据包如下：
        {
            "access_token":"ACCESS_TOKEN",
            "expires_in":7200,
            "refresh_token":"REFRESH_TOKEN",
            "openid":"OPENID",
            "scope":"SCOPE"
        }
        参数    描述
        access_token    网页授权接口调用凭证,注意：此access_token与基础支持的access_token不同
        expires_in      access_token接口调用凭证超时时间，单位（秒）
        refresh_token   用户刷新access_token
        openid  用户唯一标识，请注意，在未关注公众号时，用户访问公众号的网页，
                也会产生一个用户和公众号唯一的OpenID
        scope   用户授权的作用域，使用逗号（,）分隔
        ---------
        错误时微信会返回JSON数据包如下(示例为Code无效错误)
        {"errcode":40029,"errmsg":"invalid code"}
        """
        params = {
            'appid': self.auth.appid,
            'secret': self.auth.secret,
            'code': oauth_code,
            'grant_type': 'authorization_code'
        }
        with self._do_request('GET', '/sns/oauth2/access_token',
                              params=params) as resp_json:
            return OAuthToken(token=resp_json['access_token'],
                              openid=resp_json['openid'],
                              raw_data=resp_json)

    def get_sns_user_info(self, openid, oauth_token):
        """(公众号)文档见https://mp.weixin.qq.com/wiki?t=resource/
        res_main&id=mp1421140842
        -------
        参数    描述
        access_token
        网页授权接口调用凭证,注意：此access_token与基础支持的access_token不同
        openid  用户的唯一标识
        lang    返回国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语
        ----
        正常响应
        {
            "openid":" OPENID",
            "nickname": NICKNAME,
            "sex":"1",
            "province":"PROVINCE"
            "city":"CITY",
            "country":"COUNTRY",
            "headimgurl": "http://thirdwx.qlogo.cn/",
            "privilege":["PRIVILEGE1" "PRIVILEGE2"],
            "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
        }
        ----
        异常响应 示例为openid无效
        {"errcode":40003,"errmsg":" invalid openid "}
        """
        params = {
            'access_token': oauth_token,
            'openid': openid,
            'lang': 'zh_CN'
        }
        with self._do_request('GET', 'sns/userinfo',
                              params=params) as resp_json:
            return UserInfo(openid=resp_json['openid'],
                            unionid=resp_json['unionid'],
                            nickname=resp_json['nickname'],
                            avatar_url=resp_json['headimgurl'],
                            raw_data=resp_json)

    def get_user_info(self, openid, lang='zh_CN'):
        """获取用户基本信息， 文档见https://developers.weixin.qq.com/doc/
        offiaccount/User_Management/Get_users_basic_information_UnionID.html#UinonId
        -------------
        参数   描述
        access_token 调用接口凭证
        openid 普通用户的标识，对当前公众号唯一
        lang 返回国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语
        -------------
        响应
        {
            "subscribe": 1,
            "openid": "o6_bmjrPTlm6_2sgVt7hMZOPfL2M",
            "nickname": "Band",
            "sex": 1,
            "language": "zh_CN",
            "city": "广州",
            "province": "广东",
            "country": "中国",
            "headimgurl":"http://thirdwx.qlogo.cn/mmopen/',
            "subscribe_time": 1382694957,
            "unionid": " o6_bmasdasdsad6_2sgVt7hMZOPfL"
            "remark": "",
            "groupid": 0,
            "tagid_list":[128,2],
            "subscribe_scene": "ADD_SCENE_QR_CODE",
            "qr_scene": 98765,
            "qr_scene_str": ""
        }
        """
        params = {
            'access_token': self.auth.access_token,
            'lang': lang,
            'openid': openid
        }
        with self._do_request('GET', 'cgi-bin/user/info',
                              params=params) as resp_json:
            return resp_json

    def batch_get_user_info(self, openid_lst, lang='zh_CN'):
        """批量获取用户基本信息, 文档见https://developers.weixin.qq.com/doc/
        offiaccount/User_Management/Get_users_basic_information_UnionID.html#UinonId
        -----------------
        参数
        {
            "user_list": [  # 最多100条
                {
                    "openid": "otvxTs4dckWG7imySrJd6jSi0CWE",
                    "lang": "zh_CN"
                },
            ]
        }
        ----------------
        响应
        {
           "user_info_list": [
               {
                   "subscribe": 1,
                   "openid": "otvxTs4dckWG7imySrJd6jSi0CWE",
                   "nickname": "iWithery",
                   "sex": 1,
                   "language": "zh_CN",
                   "city": "揭阳",
                   "province": "广东",
                   "country": "中国",
                   "headimgurl": "http://thirdwx.qlogo.cn/mmopen/",
                   "subscribe_time": 1434093047,
                   "unionid": "oR5GjjgEhCMJFyzaVZdrxZ2zRRF4",
                   "remark": "",
                   "groupid": 0,
                   "tagid_list":[128,2],
                   "subscribe_scene": "ADD_SCENE_QR_CODE",
                   "qr_scene": 98765,
                   "qr_scene_str": ""
               },
               {
                   "subscribe": 0,
                   "openid": "otvxTs_JZ6SEiP0imdhpi50fuSZg"
               }
           ]
        }
        """
        if not openid_lst:
            return {}
        if len(openid_lst) > 100:
            raise ValueError('openid count should be <= 100')
        params = {'access_token': self.auth.access_token}
        data = {
            'user_list': [{
                'openid': openid,
                'lang': lang
            } for openid in openid_lst]
        }
        with self._do_request('POST',
                              'cgi-bin/user/info/batchget',
                              params=params,
                              json=data) as resp_json:
            return {
                item['openid']: item
                for item in resp_json['user_info_list']
            }

    def get_user_lst(self, next_openid=None):
        """获取用户列表， 文档见https://developers.weixin.qq.com/doc/
        offiaccount/User_Management/Getting_a_User_List.html
        -----------
        参数   描述
        access_token 调用接口凭证
        next_openid  第一个拉取的OPENID，不填默认从头开始拉取
        -----------
        响应
        {
            "total":2,  # 关注该公众账号的总用户数
            "count":2,  # 拉取的OPENID个数，最大值为10000
            "data":{
            "openid":["OPENID1","OPENID2"]},
            "next_openid":"NEXT_OPENID"
        }
        """
        params = {'access_token': self.auth.access_token}
        if next_openid:
            params['next_openid'] = next_openid
        with self._do_request('GET', 'cgi-bin/user/get',
                              params=params) as resp_json:
            return resp_json
