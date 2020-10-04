from ...messages.customer_service import CustomerServiceMessage


class CustomerServiceMixin:
    def send_custom_service_message(self, openid, message):
        """发送客服消息
        文档见: https://developers.weixin.qq.com/doc/offiaccount
        /Message_Management/Service_Center_messages.html
        """
        if not isinstance(message, CustomerServiceMessage):
            err_msg = 'message should be instance of CustomerServiceMessage, '\
                    'but get {}'.format(type(message))
            raise ValueError(err_msg)
        json_data = message.render(openid)
        params = {'access_token': self.auth.access_token}
        with self._do_request('POST',
                              '/cgi-bin/message/custom/send',
                              params=params,
                              json=json_data) as resp_json:
            return resp_json['errcode'] == 0
