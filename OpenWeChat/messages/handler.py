from .. import exceptions, logging
from ..consts import EventType, MessageType
from ..messages.reply import BlankResponse
from ..messages.request import Event, load_request


class Handler:
    def __init__(self):
        self.logger = logging.create_logger()

    def get_handler(self, request):
        if isinstance(request, Event):
            event = EventType(request.Event.lower())
            handler = self.get_event_handler(event)
            if not handler:
                self.logger.warning(
                    '[msg_type: %s] [event: %s] cannot get handler',
                    request.MsgType, request.Event)
        else:
            msg_type = MessageType(request.MsgType)
            handler = self.get_message_handler(msg_type)
            if not handler:
                self.logger.warning('[msg_type: %s] cannot get handler',
                                    request.MsgType)
        return handler

    def handle_request(self, xml_data):
        # 构造请求
        request_message, msg = load_request(xml_data)
        if not request_message:
            self.logger.error('cannot initial request message, hint: %s', msg)
            handler = self.default_handler
        else:
            handler = self.get_handler(request_message)
            handler = handler or self.default_handler
        resp_message = handler(request_message)
        # 返回响应内容
        if hasattr(resp_message, 'render'):
            resp_message = resp_message.render()
        return resp_message

    def default_handler(self, message):
        return BlankResponse()

    def get_event_handler(self, event_type):
        return None

    def get_message_handler(self, message_type):
        return None
