"""
SDKError
  +-- ImproperlyConfigured
  +-- MessageError
    +-- UnknownMessageType
    +-- UnknownEventType
  +-- ServerError
    +-- NetworkError
      +-- Timeout
    +-- InvalidResponse
    +-- APIError
      +-- ServerBusy
      +-- InvalidOAuthCode
      +-- OauthCodeAlreadyUsed
      +-- TooManyRequests
  +-- InternalError
    +-- CredentialsError
      +-- CannotGetAccessToken
        + AccessTokenDoesNotExist
        + AccessTokenIsCorrupted
      +-- CannotGetJSTicket
        +-- JSTicketDoesNotExist
        +-- JSTicketIsCorrupted
"""
from .consts.error_code import ERROR_CODE_HINT_MAPPPING


class SDKError(Exception):
    pass


class ImproperlyConfigured(SDKError):
    pass


#############################################
#  MessageError
#############################################
class MessageError(SDKError):
    pass


class UnknownMessageType(MessageError):
    pass


class UnknownEventType(MessageError):
    pass


############################################
# ServerError
############################################
class ServerError(SDKError):
    pass


class NetworkError(ServerError):
    pass


class Timeout(NetworkError):
    pass


class InvalidResponse(ServerError):
    pass


##########################################
# InternalError
##########################################
class InternalError(SDKError):
    pass


class CredentialsError(InternalError):
    pass


class CannotGetAccessToken(CredentialsError):
    pass


class AccessTokenDoesNotExist(CannotGetAccessToken):
    pass


class AccessTokenIsCorrupted(CannotGetAccessToken):
    pass


class CannotGetJSTicket(CredentialsError):
    pass


class JSTicketDoesNotExist(CannotGetJSTicket):
    pass


class JSTicketIsCorrupted(CannotGetJSTicket):
    pass


########################################
# APIError
########################################
error_code_exception_mapping = {}


class APIErrorMeta(type):
    def __new__(cls, cls_name, bases, cls_dict):
        if 'ERROR_CODE' not in cls_dict:
            raise TypeError('ERROR_CODE is expected')
        try:
            error_code = int(cls_dict['ERROR_CODE'])
        except (ValueError, TypeError):
            msg = 'ERROR_CODE must be a number, not {}'
            raise ValueError(msg.format(cls_dict['ERROR_CODE']))
        if error_code in error_code_exception_mapping:
            msg = 'ERROR_CODE {} already registered as {}'
            raise ValueError(
                msg.format(error_code,
                           error_code_exception_mapping[error_code]))
        if not cls_dict.get('ERROR_CODE_HINT'):
            cls_dict['ERROR_CODE_HINT'] = ERROR_CODE_HINT_MAPPPING.get(
                error_code)
        new_cls = super().__new__(cls, cls_name, bases, cls_dict)
        error_code_exception_mapping[error_code] = new_cls
        return new_cls


class APIError(ServerError, metaclass=APIErrorMeta):
    ERROR_CODE = 0
    ERROR_CODE_HINT = ''

    def __init__(self, error_code, resp_code, resp_content, hint=''):
        self.error_code = error_code
        self.resp_code = resp_code  # http response status code
        self.resp_content = resp_content  # http response content
        self.hint = hint

    def __str__(self):
        return '<{name}({error_code}){hint}>'.format(
            name=self.__class__.__name__,
            error_code=self.error_code,
            hint=self.hint)


def make_api_error(error_code, resp_code, resp_content, hint=''):
    cls = error_code_exception_mapping.get(error_code, APIError)
    return cls(error_code, resp_code, resp_content, hint=hint)


class ServerBusy(APIError):
    ERROR_CODE = -1


class InvalidOAuthCode(APIError):
    ERROR_CODE = 40029


class OauthCodeAlreadyUsed(APIError):
    ERROR_CODE = 40163


class TooManyRequests(APIError):
    ERROR_CODE = 45011
