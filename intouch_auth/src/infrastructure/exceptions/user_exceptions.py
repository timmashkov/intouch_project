from infrastructure.exceptions.base import BaseAPIException

from fastapi import status


class UserNotFound(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "User not found"


class UserAlreadyExist(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "User already exist"


class WrongPassword(BaseAPIException):
    status_code = status.HTTP_403_FORBIDDEN
    message = "Wrond password"


class Unauthorized(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Unauthorized"
