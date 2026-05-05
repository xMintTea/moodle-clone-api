from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from fastapi import Depends, Security

bearer_scheme = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/v1/auth/login/"
)
