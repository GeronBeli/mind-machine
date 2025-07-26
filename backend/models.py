from sqlalchemy import Column, DateTime, Float, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone

class User(Base):
    """
    Represents a user in the system.

    Attributes:
        user_id (str): The unique identifier of the user.
        is_admin (bool): Indicates whether the user is an admin or not.
        last_login (datetime): The timestamp of the user's last login.
    """
    __tablename__ = 'Users'
    user_id = Column(String, primary_key=True)
    is_admin = Column(Boolean)
    last_login = Column(DateTime, nullable=True)
    used_storage = Column(Float, default=0.0) 

    def __repr__(self):
        return f"<User(user_id={self.user_id}, is_admin={self.is_admin})>"




class SearchHistory(Base):
    """
    Represents a search history entry in the database.

    Attributes:
        id (int): The unique identifier of the search history entry.
        user_id (str): The foreign key referencing the user who made the search.
        search_query (str): The search query made by the user.
        timestamp (datetime): The timestamp of the search.
        user (User): The user who made the search.
    """
    __tablename__ = 'SearchHistory'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('Users.user_id'))
    search_query = Column(String)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))  # Timestamp for each search
    user = relationship("User")


class AdminSettings(Base):
    """
    Represents the admin settings in the database.

    Attributes:
        id (int): The primary key for the admin settings.
        logout_timer (float): The logout timer in seconds or any other unit.
        max_disk_space (float): The maximum disk space in MB or any other unit.
        user_max_disk_space (float): The maximum disk space for each user in MB or any other unit.
    """
    __tablename__ = 'AdminSettings'
    id = Column(Integer, primary_key=True)
    logout_timer = Column(Float)  # Logout timer in seconds or any other unit
    max_disk_space = Column(Float)  # Max disk space in MB or any other unit
    user_max_disk_space = Column(Float)
    #user = relationship("User", back_populates="settings")