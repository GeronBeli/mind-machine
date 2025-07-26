from typing import Annotated
from fastapi import HTTPException
import os
from database import DbSession
import config
from ldap3 import Server, Connection
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import status, Depends
from fastapi.security import OAuth2PasswordBearer
from .user_service import get_user, init_user  

secret_key = os.getenv("JWT_SECRET_KEY", "fallback_secret")
algorithm = 'HS256'
oath2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

def authenticate_user(user_id: str, password: str, db: DbSession):
    ldap_server = Server(config.ldap_server)
    base_dn = config.base_dn
    username = f'cn={user_id},ou=idmusers,' + base_dn

    conn = Connection(ldap_server, user=username, password=password, auto_bind=False)
    conn.start_tls()

    if not conn.bind():
        return None
    
    try:
        user = get_user(db, user_id)
    except ValueError:
        init_user(db, user_id, False)
        user = get_user(db, user_id)
    
    return user

def create_access_token(user_id: str, is_admin: bool, expires_delta: timedelta):
    payload = {'sub': user_id, 'is_admin': is_admin, 'exp': datetime.now(timezone.utc) + expires_delta}
    return jwt.encode(payload, secret_key, algorithm=algorithm)

def decode_token(token: str):
    return jwt.decode(token, secret_key, algorithms=[algorithm])

async def get_current_user(token: Annotated[str, Depends(oath2_bearer)]):
    try:
        payload = decode_token(token)
        user_id = payload.get('sub')
        is_admin = payload.get('is_admin', False)
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="Could not validate credentials")
        return {'user_id': user_id, 'is_admin': is_admin}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Could not validate credentials")