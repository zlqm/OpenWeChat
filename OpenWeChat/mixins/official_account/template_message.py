class TemplateMessageMixin:
    def send_template_message(self, openid, template_id, data, page_url):
        """发送模板消息
        接口文档见 https://developers.weixin.qq.com/doc/offiaccount
        /Message_Management/Template_Message_Interface.html#5
        --------------
        参数
        {
            "touser":"OPENID",
            "template_id":"ngqIpbwh8bUfcSsECmogfXcV14J0tQlEpBO27izEYtY",
            "url":"http://weixin.qq.com/download",
            "miniprogram":{
              "appid":"xiaochengxuappid12345",
              "pagepath":"index?foo=bar"
            },
            "data":{
                 "first": {
                     "value":"恭喜你购买成功！",
                     "color":"#173177"
                 },
                 "keyword1":{
                     "value":"巧克力",
                     "color":"#173177"
                 },
                 "keyword2": {
                     "value":"39.8元",
                     "color":"#173177"
                 },
                 "keyword3": {
                     "value":"2014年9月22日",
                     "color":"#173177"
                 },
                 "remark":{
                     "value":"欢迎再次购买！",
                     "color":"#173177"
                 }
            }
        }

        参数说明
        参数    是否必填    说明
        touser  是  接收者openid
        template_id     是  模板ID
        url     否  模板跳转链接（海外帐号没有跳转能力）
        miniprogram     否  跳小程序所需数据，不需跳小程序可不用传该数据
        appid   是
        所需跳转到的小程序appid（该小程序appid必须与发模板消息的公众号是绑定关联关系，暂不支持小游戏）
        pagepath    否
        所需跳转到小程序的具体页面路径，支持带参数,（示例index?foo=bar），要求该小程序已发布，暂不支持小游戏
        data    是  模板数据
        color   否  模板内容字体颜色，不填默认为黑色
        ------------------------
        响应
        {
             "errcode":0,
             "errmsg":"ok",
             "msgid":200228332
        }
        """
        params = {
            'access_token': self.auth.access_token,
        }
        json_data = {
            'touser': openid,
            'template_id': template_id,
            'url': page_url,
            'data': data,
        }
        with self._do_request(
                'POST', '/cgi-bin/message/template/send', params=params,
                json=json_data) as resp_json:
            return resp_json['msgid']

