from models import User, SearchHistory, AdminSettings
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: str):
        return self.db.query(User).filter(User.user_id == user_id).first()

    def add(self, user: User):
        self.db.add(user)
        self.db.commit()

    def delete(self, user: User):
        self.db.delete(user)
        self.db.commit()

    def update_last_login(self, user: User):
        user.last_login = datetime.now(timezone.utc)
        self.db.commit()

    def get_active_users_count(self):
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
        return self.db.query(User).filter(User.last_login >= thirty_days_ago).count()

    def get_inactive_users_count(self):
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
        return self.db.query(User).filter(User.last_login < thirty_days_ago).count()



class SearchRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_search_history(self, user_id):
        return self.db.query(SearchHistory)\
                .filter(SearchHistory.user_id == user_id)\
                .order_by(SearchHistory.timestamp.desc())\
                .all()

    def count_recent_searches(self, since_time):
        return self.db.query(SearchHistory).filter(SearchHistory.timestamp >= since_time).count()

    def add_search(self, search_history):
        self.db.add(search_history)
        self.db.commit()

    def delete_oldest_search(self, user_id):
        oldest = (self.db.query(SearchHistory)
                  .filter(SearchHistory.user_id == user_id)
                  .order_by(SearchHistory.timestamp.asc())
                  .first())
        if oldest:
            self.db.delete(oldest)
            self.db.commit()


