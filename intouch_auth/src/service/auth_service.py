from fastapi import Depends

from service.auth_handler import AuthHandler


class AuthService:
    def __init__(self, auth_repo: AuthHandler = Depends(AuthHandler)):
        pass
