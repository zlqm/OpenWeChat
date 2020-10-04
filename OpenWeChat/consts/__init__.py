from enum import Enum


class AppType(Enum):
    OFFICIAL_ACCOUNT = 'official_account'  # 公众号
    MINI_PROGRAM = 'mini_program'  # 小程序


class MediaType(Enum):
    IMAGE = 'image'
    VOICE = 'voice'
    VIDEO = 'video'
    THUMB = 'thumb'


class MessageType(Enum):
    TEXT = 'text'  # 文本消息
    LINK = 'link'  # 链接
    EVENT = 'event'  # 事件
    IMAGE = 'image'  # 图片消息
    VOICE = 'voice'  # 语音
    LOCATION = 'location'  # 地理位置
    SHORT_VIDEO = 'short_video'  # 短视频
    NEWS = 'news'  # 图文消息
    MUSIC = 'music'  # 音乐消息


class EventType(Enum):
    SCAN = 'scan'  # 扫描带参数二维码事件
    VIEW = 'view'  # 通过菜单打开页面
    CLICK = 'click'  # 菜单点击事件
    LOCATION = 'location'  # 上报地理位置事件
    SUBSCRIBE = 'subscribe'  # 关注
    UNSUBSCRIBE = 'unsubscribe'  # 取关
    TEMPLATESENDJOBFINISH = 'templatesendjobfinish'  # 模板消息发送完成
    SCANCODE_PUSH = 'scancode_push'  # 扫码推事件的事件推送
    SCANCODE_WAITING = 'scancode_waitmsg'  # 扫码推事件且弹出“消息接收中”提示框的事件推送
    PIC_SYSPHOTO = 'pic_sysphoto'  # 弹出系统拍照发图的事件推送
    PIC_PHOTO_OR_ALBUM = 'pic_photo_or_album'  # 弹出拍照或者相册发图的事件推送
    PIC_WEIXIN = 'pic_weixin'  # 弹出微信相册发图器的事件推送
    LOCATION_SELECT = 'location_select'  # 弹出地理位置选择器的事件推送
    VIEW_MINIPROGRAM = 'view_miniprogram'  # 点击菜单跳转小程序的事件推送
