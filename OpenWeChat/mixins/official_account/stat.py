from datetime import timedelta

TIME_FORMAT = '%Y-%m-%d'


class StatMixin:
    def get_user_summary(self, from_date, to_date, max_day_delta=7):
        """统计用户增长情况
        文档见: https://developers.weixin.qq.com/doc/
        offiaccount/Analytics/User_Analysis_Data_Interface.html
        --------
        参数     描述
        access_token  调用接口凭证
        begin_date  获取数据的起始日期，begin_date和end_date的差值
                    需小于“最大时间跨度(7)”
        end_date  获取数据的结束日期，end_date允许设置的最大值为昨日
        --------
        响应数据
        {
            "list": [
                {
                    "ref_date": "2014-12-07",
                    "user_source": 0,
                    "new_user": 0,
                    "cancel_user": 0
                }//后续还有ref_date在begin_date和end_date之间的数据
            ]
        }
        """
        if to_date - from_date > timedelta(days=max_day_delta):
            raise ValueError(
                'date range should be <= {}'.format(max_day_delta))
        from_date = from_date.strftime(TIME_FORMAT)
        to_date = to_date.strftime(TIME_FORMAT)
        params = {
            'access_token': self.auth.access_token,
        }
        data = {'begin_date': from_date, 'end_date': to_date}
        with self._do_request('POST',
                              '/datacube/getusersummary',
                              params=params,
                              json=data) as resp_json:
            return resp_json['list']

    def get_user_cumulate(self, from_date, to_date, max_day_delta=7):
        """获取累计用户数据
        文档见: https://developers.weixin.qq.com/doc/
        offiaccount/Analytics/User_Analysis_Data_Interface.html
        --------
        参数     描述
        access_token  调用接口凭证
        begin_date  获取数据的起始日期，begin_date和end_date的差值
                    需小于“最大时间跨度(7)”
        end_date  获取数据的结束日期，end_date允许设置的最大值为昨日
        --------
        响应数据
        {
            "list": [
                {
                    "ref_date": "2014-12-07",
                    "cumulate_user": 1217056
                }, //后续还有ref_date在begin_date和end_date之间的数据
            ]
        }
        """
        if to_date - from_date > timedelta(days=max_day_delta):
            raise ValueError(
                'date range should be <= {}'.format(max_day_delta))
        from_date = from_date.strftime(TIME_FORMAT)
        to_date = to_date.strftime(TIME_FORMAT)
        params = {
            'access_token': self.auth.access_token,
        }
        data = {'begin_date': from_date, 'end_date': to_date}
        with self._do_request('POST',
                              '/datacube/getusercumulate',
                              params=params,
                              json=data) as resp_json:
            return resp_json['list']
