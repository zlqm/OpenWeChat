import hashlib
import string
import time
try:
    from secrets import choice as random_choice
except ImportError:
    # 兼容py3.5
    from random import SystemRandom
    _sysrand = SystemRandom()
    random_choice = _sysrand.choice


def create_nonce_str():
    return ''.join(
        random_choice(string.ascii_letters + string.digits) for _ in range(15))


def generate_js_sdk_sign(js_ticket, url):
    """
    文档见: https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421141115
    签名生成规则如下：参与签名的字段包括noncestr（随机字符串）,
    有效的jsapi_ticket, timestamp（时间戳）, url（当前网页的URL，不包含#及其后面部分）。
    对所有待签名参数按照字段名的ASCII码从小到大排序（字典序）后，
    使用URL键值对的格式（即key1=value1&key2=value2…）拼接成字符串string1。
    这里需要注意的是所有参数名均为小写字符。
    对string1作sha1加密，字段名和字段值都采用原始值，不进行URL转义。
    """
    # 这里的变量名有驼峰有下划线。。
    data = {
        'nonceStr': create_nonce_str(),  # 此处的nonceStr为驼峰命名
        'jsapi_ticket': js_ticket,
        'timestamp': int(time.time()),
        'url': url
    }
    items = sorted(data.items(), key=lambda item: item[0])
    # 注意，这里有lower
    text = '&'.join('{}={}'.format(item[0].lower(), item[1]) for item in items)
    data['signature'] = hashlib.sha1(text.encode()).hexdigest()
    data.pop('jsapi_ticket')
    return data


class JSSDKMixin:
    def generate_js_sdk_sign(self, url):
        """生成H5端需要的js Service sign
        """
        js_ticket = self.auth.js_ticket
        return generate_js_sdk_sign(js_ticket, url)
