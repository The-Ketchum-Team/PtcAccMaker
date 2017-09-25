# Script architecture based on PTCAccount by jepayne1138

__all__ = [
    'PTCException',
    'PTCInvalidStatusCodeException',
    'PTCInvalidNameException',
    'PTCInvalidEmailException',
    'PTCInvalidPasswordException',
    'PTCInvalidBirthdayException',
]


class PTCException(Exception):
    """Base exception for all PTC Account exceptions"""
    pass


class PTCInvalidStatusCodeException(Exception):
    """Base exception for all PTC Account exceptions"""
    pass


class PTCInvalidNameException(PTCException):
    """Username already in use"""
    pass


class PTCInvalidEmailException(PTCException):
    """Email invalid or already in use"""
    pass


class PTCInvalidPasswordException(PTCException):
    """Password invalid"""
    pass


class PTCInvalidBirthdayException(PTCException):
    """Birthday invalid"""
    pass
