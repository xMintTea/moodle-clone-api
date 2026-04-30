from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, Security

bearer_schema = HTTPBearer()
