class CloudflarepyException(Exception):
    pass


class APIException(CloudflarepyException):
    def __init__(self, code: int, message: str):
        super().__init__(f"API 에러가 발생하였습니다 {code} - {message}")


class AuthException(CloudflarepyException):
    def __init__(self):
        super().__init__("로그인에 실패하였습니다")

class ForbiddnException(CloudflarepyException):
    def __init__(self):
        super().__init__("권한이 없습니다")

class RateLimitException(CloudflarepyException):
    def __init__(self):
        super().__init__("요청이 너무 많습니다")

class BadRequestException(CloudflarepyException):
    def __init__(self):
        super().__init__("잘못된 요청입니다")

class NotModifiedException(CloudflarepyException):
    def __init__(self):
        super().__init__("변경사항이 없습니다")


class MethodNotAllowedException(CloudflarepyException):
    def __init__(self):
        super().__init__("허용되지 않는 메소드입니다")

class UnsupportedMediaTypeException(CloudflarepyException):
    def __init__(self):
        super().__init__("지원하지 않는 미디어 타입입니다")

Exceptions = {
    304: NotModifiedException,
    400: BadRequestException,
    401: AuthException,
    403 : ForbiddnException,
    429: RateLimitException,
    405: MethodNotAllowedException,
    415: UnsupportedMediaTypeException
}
