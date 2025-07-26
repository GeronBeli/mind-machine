from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from services.auth_service import authenticate_user, create_access_token
from services.user_service import get_user, update_last_login
from services.admin_settings_service import get_settings
from datetime import timedelta
from schemas import Token
import logging
from database import DbSession

auth_router = APIRouter(prefix='/auth',tags=['auth'])



@auth_router.post('/token', response_model=Token)
async def get_access_token(db: DbSession, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail='Could not validate credentials')

    update_last_login(db,user.user_id)

    if user.is_admin:
        logging.info(f"User {user.user_id} logged in as admin")
        
    else:
        logging.info(f"User {user.user_id} logged in as user")
        
    
    timeout = get_settings(db).logout_timer
    token = create_access_token(user.user_id, user.is_admin, timedelta(minutes=timeout))
    return {'access_token': token, 'token_type': 'bearer', 'is_admin': user.is_admin}