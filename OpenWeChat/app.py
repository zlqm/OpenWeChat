from .base import Base
from .mixins import auth, mini_program, official_account


class SDK(Base, auth.CredentialsMixin):
    pass


class MiniProgram(SDK, mini_program.MiniProgramMixin):
    pass


class OfficialAccount(SDK, official_account.OfficialAccountMixin):
    pass
