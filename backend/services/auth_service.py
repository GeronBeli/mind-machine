from fastapi import HTTPException
import os
import config
from ldap3 import Server, Connection
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from user_service import UserService
from fastapi import status

class AuthService:
    def __init__(self, user_srv: UserService):
        self.user_srv = user_srv
        self.secret_key = os.getenv("JWT_SECRET_KEY", "fallback_secret")
        self.algorithm = 'HS256'

    def authenticate_user(self, user_id: str, password: str):
        ldap_server = Server(config.ldap_server)
        base_dn = config.base_dn
        username = f'cn={user_id},ou=idmusers,' + base_dn

        conn = Connection(ldap_server, user=username, password=password, auto_bind=False)
        conn.start_tls()

        if not conn.bind():
            return None
        
        user = self.user_srv.get_user(user_id)
        if user is None:
            self.user_srv.init_user(user_id, False)
            user = self.user_srv.get_user(user_id)
        
        return user

    def create_access_token(self, user_id: str, is_admin: bool, expires_delta: timedelta):
        payload = {'sub': user_id, 'is_admin': is_admin, 'exp': datetime.now(timezone.utc) + expires_delta}
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str):
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
    

    # Async method to get user from token
    async def get_user_from_token(self, token: str):
        try:
            payload = self.decode_token(token)
            user_id = payload.get('sub')
            if user_id is None:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated")
            return self.user_srv.get_user(user_id)
        except JWTError:
            raise JWTError("Invalid token")