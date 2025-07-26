from models import User
from datetime import datetime, timezone, timedelta
from database import DbSession

def init_user(db: DbSession, user_id, is_admin=False):
    user = db.query(User).filter(User.user_id == user_id).first()

    if user:
        return
    new_user = User(user_id=user_id, is_admin=is_admin)
    db.add(new_user)
    db.commit()

def get_user(db: DbSession, user_id):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise ValueError("User not found")
    return user

def get_all_users(db: DbSession)-> list[User]:
    return db.query(User).all()

def delete_user(db: DbSession, user_id):
    user = get_user(db, user_id)
    db.delete(user)

def update_last_login(db: DbSession, user_id):
    user = get_user(db, user_id)
    user.last_login = datetime.now(timezone.utc)
    db.commit()

def get_active_users_count(db: DbSession):
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    return db.query(User).filter(User.last_login > thirty_days_ago).count()
    
def get_inactive_users_count(db: DbSession):
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    return db.query(User).filter(User.last_login < thirty_days_ago).count()
     
