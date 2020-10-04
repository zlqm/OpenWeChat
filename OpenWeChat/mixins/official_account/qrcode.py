class QRCodeMixin:
    def create_qrcode(self,
                      value,
                      _type='QR_LIMIT_STR_SCENE',
                      expire_seconds=None):
        """创建事件二维码
        文档见: https://developers.weixin.qq.com/doc/offiaccount/
        Account_Management/Generating_a_Parametric_QR_Code.html
        --------------------------------
        参数
        参数 说明
        expire_seconds 该二维码有效时间，以秒为单位。
        最大不超过2592000（即30天），此字段如果不填，则默认有效期为30秒。
        action_name
        二维码类型，QR_SCENE为临时的整型参数值，QR_STR_SCENE为临时的字符串参数值，QR_LIMIT_SCENE为永久的整型参数值，QR_LIMIT_STR_SCENE为永久的字符串参数值
        action_info 二维码详细信息
        scene_id
        场景值ID，临时二维码时为32位非0整型，永久二维码时最大值为100000（目前参数只支持1--100000）
        scene_str 场景值ID（字符串形式的ID），字符串类型，长度限制为1到64
        ----------------------
        响应数据
        {"ticket":"gQH473sUw==","expire_seconds":60,"url":"http://weixin.qq.com/q/kZgfwMTm72WWPkovabbI"}
        """
        params = {
            'access_token': self.auth.access_token,
        }
        json_data = {'action_name': _type, 'action_info': {'scene': {}}}
        if _type in ['QR_SCENE', 'QR_STR_SCENE']:
            json_data['action_info']['scene']['scene_id'] = value
        else:
            json_data['action_info']['scene']['scene_str'] = value
        if _type in ['QR_SCENE', 'QR_STR_SCENE']:
            if not expire_seconds:
                raise ValueError(
                    'invalid expire_seconds: {}'.format(expire_seconds))
            json_data['expire_seconds'] = expire_seconds
        with self._do_request('POST',
                              '/cgi-bin/qrcode/create',
                              params=params,
                              json=json_data) as resp_json:
            return resp_json
