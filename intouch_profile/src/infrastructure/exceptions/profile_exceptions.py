from intouch_profile.src.infrastructure.exceptions.base import BaseAPIException

from fastapi import status


class ProfileNotFound(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Profile not found"


class ProfileAlreadyExist(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Profile already exist"
