from .. import consts, exceptions
from ..helpers import Int, Str, Schema, walk_subclass, get_xml_node_value

_message_cls_mapping = {}
_event_cls_mapping = {}


def register_request(msg_type=None, event_type=None):
    def wrapper(cls):
        global _message_cls_mapping, _event_cls_mapping
        if msg_type:
            _message_cls_mapping[msg_type] = cls
        if event_type:
            _event_cls_mapping[event_type] = cls
        return cls

    return wrapper


def load_request(xml_data):
    """parse raw request from wechat to Request instance
    """
    global _message_cls_mapping, _event_cls_mapping
    try:
        msg_type = get_xml_node_value(xml_data, 'MsgType')
        msg_type = consts.MessageType(msg_type)
    except KeyError:
        return None, 'cannot get node MsgType'
    except ValueError:
        return None, 'unknown msg_type {}'.format(msg_type)
    if msg_type is consts.MessageType.EVENT:
        try:
            event_type = get_xml_node_value(xml_data, 'Event')
            event_type = event_type.lower()
            event_type = consts.EventType(event_type)
            request_cls = _event_cls_mapping.get(event_type)
        except KeyError:
            return None, 'cannot get node Event'
        except ValueError:
            return None, 'unknown event {}'.format(event_type)
    else:
        request_cls = _message_cls_mapping.get(msg_type)
    if request_cls:
        return request_cls.from_xml_data(xml_data), ''
    return None, 'cannot get request cls'


class Request(Schema):
    ToUserName = Str()
    FromUserName = Str()
    CreateTime = Int()
    MsgType = Str()

    @classmethod
    def from_xml_data(cls, xml_data):
        kwargs = {}
        for key in cls._data_fields:
            try:
                kwargs[key] = get_xml_node_value(xml_data, key)
            except KeyError:
                pass
        return cls(**kwargs)


class Message(Request):
    pass


@register_request(msg_type=consts.MessageType.TEXT)
class TextMessage(Message):
    Content = Str()
    # 用户接收到 客服-菜单-消息，点击选项后，微信会回调点击信息
    # 文档见https://developers.weixin.qq.com/doc/offiaccount/
    # Message_Management/Service_Center_messages.html
    bizmsgmenuid = Str(default=None)


@register_request(msg_type=consts.MessageType.LINK)
class LinkMessage(Message):
    Title = Str()
    Description = Str()
    Url = Str()


@register_request(msg_type=consts.MessageType.IMAGE)
class ImageMessage(Message):
    PicUrl = Str()
    MediaId = Str()


@register_request(msg_type=consts.MessageType.VOICE)
class VoiceMessage(Message):
    MediaId = Str()
    Format = Str()


@register_request(msg_type=consts.MessageType.LOCATION)
class LocationMessage(Message):
    LocationX = Str()
    LocationY = Str()
    Scale = Str()
    Label = Str()


class Event(Request):
    Event = Str()


class EventWithKey(Event):
    EventKey = Str()


@register_request(event_type=consts.EventType.SCAN)
class ScanEvent(EventWithKey):
    Ticket = Str()


@register_request(event_type=consts.EventType.VIEW)
class ViewEvent(EventWithKey):
    pass


@register_request(event_type=consts.EventType.LOCATION)
class LocationEvent(Event):
    Latitude = Str()
    Longtude = Str()
    Precision = Str()


@register_request(event_type=consts.EventType.SUBSCRIBE)
class SubscribeEvent(EventWithKey):
    pass


@register_request(event_type=consts.EventType.UNSUBSCRIBE)
class UnSubscribeEvent(EventWithKey):
    pass


@register_request(event_type=consts.EventType.TEMPLATESENDJOBFINISH)
class TemplateSendJobFinishEvent(EventWithKey):
    pass


@register_request(event_type=consts.EventType.SCANCODE_PUSH)
class ScanCodePushEvent(EventWithKey):
    ScanCodeInfo = Str()
    ScanType = Str()
    ScanResult = Str()


@register_request(event_type=consts.EventType.SCANCODE_WAITING)
class ScanCodeWaitingEvent(ScanCodePushEvent):
    pass


@register_request(event_type=consts.EventType.LOCATION_SELECT)
class LocationSelectEvent(EventWithKey):
    Location_X = Str()
    Location_Y = Str()
    Scale = Str()
    Label = Str()
    Poiname = Str()


@register_request(event_type=consts.EventType.VIEW_MINIPROGRAM)
class ViewMiniProgramEvent(EventWithKey):
    pass
