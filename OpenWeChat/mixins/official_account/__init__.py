from . import user
from . import customer_service_message
from . import menu
from . import js_sdk
from . import media
from . import callback_handler
from . import qrcode
from . import stat
from . import template_message


class OfficialAccountMixin(
        user.UserMixin,
        customer_service_message.CustomerServiceMixin,
        menu.MenuMixin,
        js_sdk.JSSDKMixin,
        media.MediaMixin,
        callback_handler.CallbackHandlerMixin,
        qrcode.QRCodeMixin,
        stat.StatMixin,
        template_message.TemplateMessageMixin,
):
    pass
