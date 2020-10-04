"""
客服消息，文档见：https://developers.weixin.qq.com/doc/
offiaccount/Message_Management/Service_Center_messages.html
"""
import abc


class CustomerServiceMessage(abc.ABC):
    MESSAGE_TYPE = None

    @abc.abstractmethod
    def get_context(self):
        pass

    def render(self, to_user):
        data = {'touser': to_user, 'msgtype': self.MESSAGE_TYPE}
        context = self.get_context()
        data.update(**context)
        return data


class TextMessage(CustomerServiceMessage):
    MESSAGE_TYPE = 'text'

    def __init__(self, content):
        self.content = content

    def get_context(self):
        return {'text': {'content': self.content}}


class MediaMessage(CustomerServiceMessage):
    def __init__(self, media_id):
        self.media_id = media_id

    def get_context(self):
        return {self.MESSAGE_TYPE: {'media_id': self.media_id}}


class ImageMessage(MediaMessage):
    MESSAGE_TYPE = 'image'


class VoiceMessage(MediaMessage):
    MESSAGE_TYPE = 'voice'


class VideoMessage(CustomerServiceMessage):
    MESSAGE_TYPE = 'video'

    def __init__(self, media_id, thumb_media_id, title, description):
        self.media_id = media_id
        self.thumb_media_id = thumb_media_id
        self.title = title
        self.description = description

    def get_context(self):
        return {
            'video': {
                'media_id': self.media_id,
                'thumb_media_id': self.thumb_media_id,
                'title': self.title,
                'description': self.description
            }
        }


class MusicMessage(CustomerServiceMessage):
    MESSAGE_TYPE = 'music'

    def __init__(self, thumb_media_id, music_url, hq_music_url, title,
                 description):
        self.thumb_media_id = thumb_media_id
        self.music_url = music_url
        self.hq_music_url = hq_music_url
        self.title = title
        self.description = description

    def get_context(self):
        return {
            'music': {
                'title': self.title,
                'description': self.description,
                'musicurl': self.music_url,
                'hqmusicurl': self.hq_music_url,
                'thumb_media_id': self.thumb_media_id
            }
        }


class NewsMessage(CustomerServiceMessage):
    MESSAGE_TYPE = 'news'

    def __init__(self, title, description, url, pic_url):
        self.title = title
        self.description = description
        self.url = url
        self.pic_url = pic_url

    def get_context(self):
        return {
            'news': {
                'articles': [{
                    'title': self.title,
                    'description': self.description,
                    'url': self.url,
                    'picurl': self.pic_url
                }]
            }
        }


class MenuMessage(CustomerServiceMessage):
    MESSAGE_TYPE = 'msgmenu'

    def __init__(self, head_content, choices, tail_content):
        """choices为
        {'id': 1, 'content': '满意'}] 或 [(1, '满意')]
        """
        self.head_content = head_content
        self.tail_content = tail_content
        if isinstance(choices, dict):
            self.choices = [{
                'id': choice['id'],
                'content': choice['content']
            } for choice in choices]
        else:
            self.choices = [{
                'id': choice[0],
                'content': choice[1]
            } for choice in choices]

    def get_context(self):
        return {
            'msgmenu': {
                'head_content': self.head_content,
                'list': self.choices,
                'tail_content': self.tail_content
            }
        }
