class BaseCustomException(Exception):
    def __init__(self, msg: str = ""):
        self.msg = msg

    def __str__(self):
        return self.msg


class ThirdPartyCommunicationException(BaseCustomException):
    HTTP_CODE = 409
    ERROR = "fail_communicate_with_out_service"


class UnexpectedDataException(BaseCustomException):
    HTTP_CODE = 409
    ERROR = "invalid_data_format"


class RepoException(BaseCustomException):
    HTTP_CODE = 500
    ERROR = "internal_error_occur"


class FailUseCaseLogicException(BaseCustomException):
    HTTP_CODE = 409
    ERROR = "fail_in_use_case"


class NotFoundException(BaseCustomException):
    HTTP_CODE = 404
    ERROR = "not_found_resource"
