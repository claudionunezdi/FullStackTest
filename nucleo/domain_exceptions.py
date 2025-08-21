class DomainError(Exception):
    """BAse para errores de negocios"""


class AccountNotActive(DomainError):
    pass

class InsufficientFunds(DomainError):
    pass

class AmountOutOfPolicy(DomainError):
    pass

class DailyLimitExceeded(DomainError):
    pass


class DuplicateRequest(DomainError):
    """La misma operación se realizó"""

    pass

