from collections import namedtuple
import string
import time

from ..consts import MessageType


class ResponseMessage:
    MESSAGE_TYPE = None
    TEMPLATE = None

    def __init__(self, request_message, content):
        self.context = self.get_context(request_message)

    def get_context(self, request_message):
        return {
            'to_user_name': request_message.FromUserName,
            'from_user_name': request_message.ToUserName,
            'create_time': int(time.time()),
        }

    def render(self):
        return self.TEMPLATE.substitute(**self.context)


class BlankResponse(ResponseMessage):
    def __init__(self, *args, **kwargs):
        pass

    def render(self):
        return 'success'


class TextResponse(ResponseMessage):
    MESSAGE_TYPE = MessageType.TEXT
    TEMPLATE = string.Template('''<xml>
        <ToUserName><![CDATA[$to_user_name]]></ToUserName>
        <FromUserName><![CDATA[$from_user_name]]></FromUserName>
        <CreateTime>$create_time</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[$content]]></Content>
    </xml>''')

    def __init__(self, request_message, content):
        super().__init__(request_message, content)
        self.context['content'] = content


class ImageResponse(ResponseMessage):
    MESSAGE_TYPE = MessageType.TEXT
    TEMPLATE = string.Template('''<xml>
        <ToUserName><![CDATA[$to_user_name]]></ToUserName>
        <FromUserName><![CDATA[$from_user_name]]></FromUserName>
        <CreateTime>{$create_time}</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <Image>
            <MediaId><![CDATA[$media_id]]></MediaId>
        </Image>
    </xml>''')

    def __init__(self, request_message, media_id):
        super().__init__(request_message, media_id)
        self.context['media_id'] = media_id


class VoiceResponse(ResponseMessage):
    MESSAGE_TYPE = MessageType.VOICE


class MusicResponse(ResponseMessage):
    MESSAGE_TYPE = MessageType.MUSIC


class NewsResponse(ResponseMessage):
    MESSAGE_TYPE = MessageType.NEWS
    TEMPLATE = string.Template('''<xml>
        <ToUserName><![CDATA[$to_user_name]]></ToUserName>
        <FromUserName><![CDATA[$from_user_name]]></FromUserName>
        <CreateTime>$create_time</CreateTime>
        <MsgType><![CDATA[news]]></MsgType>
        <ArticleCount>$article_count</ArticleCount>
        <Articles>$articles</Articles>
    </xml>''')

    ARTICLE_TEMPLATE = '''<item>
        <Title><![CDATA[{title}]]></Title>
        <Description><![CDATA[{description}]]></Description>
        <PicUrl><![CDATA[{picurl}]]></PicUrl>
        <Url><![CDATA[{url}]]></Url>
    </item>'''

    Article = namedtuple('Article', ['title', 'description', 'picurl', 'url'])

    def __init__(self, request_message, article_lst):
        super().__init__(request_message, article_lst)
