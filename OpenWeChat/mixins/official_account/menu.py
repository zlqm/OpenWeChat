class MenuMixin:
    def update_menu(self, menu_data):
        """更新公众号菜单
        文档见: https://developers.weixin.qq.com/doc/offiaccount/
        Custom_Menus/Creating_Custom-Defined_Menu.html
        ----------
        参数
        参数    是否必须    说明
        button  是  一级菜单数组，个数应为1~3个
        sub_button  否  二级菜单数组，个数应为1~5个
        type    是
        菜单的响应动作类型，view表示网页类型，click表示点击类型，miniprogram表示小程序类型
        name    是  菜单标题，不超过16个字节，子菜单不超过60个字节
        key     click等点击类型必须
        菜单KEY值，用于消息接口推送，不超过128字节
        url     view、miniprogram类型必须   网页
        链接，用户点击菜单可打开链接，不超过1024字节。
        type为miniprogram时，不支持小程序的老版本客户端将打开本url。
        media_id    media_id类型和view_limited类型必须
        调用新增永久素材接口返回的合法media_id
        appid   miniprogram类型必须     小程序的appid（仅认证公众号可配置）
        pagepath    miniprogram类型必须     小程序的页面路径
        ----------
        正确响应时JSON数据包如下：
        {"errcode":0,"errmsg":"ok"}
        异常响应时如下:
        {"errcode":40018,"errmsg":"invalid button name size"}
        """
        params = {'access_token': self.auth.access_token}
        with self._do_request('POST',
                              '/cgi-bin/menu/create',
                              params=params,
                              json=menu_data) as resp_json:
            return resp_json['errcode'] == 0

    def get_current_menu(self):
        """获取公众号菜单
        文档见: https://developers.weixin.qq.com/doc/offiaccount/
        Custom_Menus/Querying_Custom_Menus.html
        """
        params = {'access_token': self.auth.access_token}
        with self._do_request('GET',
                              'cgi-bin/get_current_selfmenu_info',
                              params=params) as resp_json:
            return resp_json

    def delete_menu(self):
        """删除公众号菜单
        文档见: https://developers.weixin.qq.com/doc/offiaccount/
        Custom_Menus/Deleting_Custom-Defined_Menu.html
        请注意，在个性化菜单时，调用此接口会删除默认菜单及全部个性化菜单。
        """
        params = {'access_token': self.auth.access_token}
        with self._do_request('GET', '/cgi-bin/menu/delete',
                              params=params) as resp_json:
            return resp_json['errcode'] == 0
