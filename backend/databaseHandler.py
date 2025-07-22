from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, timedelta
import os
import config
from logHandler import LogHandler
from models import User, SearchHistory, AdminSettings
from contextlib import contextmanager

Base = declarative_base()



class DatabaseHandler:
    """
    A class that handles the database operations for the application.

    Attributes:
        logger: The logger object for logging messages.
        database_directory: The directory where the database is stored.
        engine: The database engine for connecting to the database.
        Session: The session object for interacting with the database.

    Methods:
        __init__: Initializes the DatabaseHandler object.
        inital_admin_settings: Initializes the admin settings.
        create_connection: Creates a connection to the database.
        check_for_user: Checks if a user exists.
        add_user: Adds a new user to the database.
        get_user: Retrieves a user from the database.
        get_all_users: Retrieves all users from the database.
        update_user: Updates a user in the database.
        delete_user: Deletes a user from the database.
        get_number_of_asked_questions: Retrieves the number of asked questions.
        get_search_history: Retrieves the search history for a user.
        log_search: Logs a search for a user.
        get_admin_settings: Retrieves the admin settings.
        update_admin_settings: Updates the admin settings.
        update_last_login: Updates the last login time for a user.
        get_active_users: Retrieves the number of active users.
        get_inactive_users: Retrieves the number of inactive users.
        test_admin_settings: Tests the admin settings functionality.
    """

    def __init__(self, data_directory, database_name):
        """
        Initializes the DatabaseHandler object.

        Args:
            data_directory (str): The directory where the database will be stored.
            database_name (str): The name of the database.
        """
        self.logger = LogHandler(name="DatabaseHandler").get_logger()
        self.database_directory = os.path.join(data_directory, database_name)
        self.create_connection()
        self.inital_admin_settings()
        #User.settings = relationship("UserSettings", back_populates="user", uselist=False)

    def inital_admin_settings(self):
        """
        Initializes the admin settings.

        This method checks if the admin settings exist in the database. If not, it creates a new entry with default values.
        """
        self.logger.debug("Initializing admin settings")
        
        settings = self.get_admin_settings()
        
        if settings is None:
            settings = AdminSettings(logout_timer=config.logout_timer, max_disk_space=config.max_disk_space, user_max_disk_space=config.user_max_disk_space)
            with self.get_db() as session:
                session.add(settings)
                session.commit()
        

    def create_connection(self):
        """
        Creates a database connection.

        This method configures the database connection and creates the necessary tables if they don't exist.
        """
        self.logger.debug("Creating database connection")
        # Configure the database connection
        self.engine = create_engine(f'sqlite:///{self.database_directory}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine, autocommit = False, autoflush=False)


    @contextmanager
    def get_db(self):
        db = self.Session()
        try:
            yield db
        finally:
            db.close()
    
    
    
    
    # CRUD operations using SQLAlchemy ORM

    


    def check_for_user(self, user_id):
        """
        Check if a user exists in the database.

        Args:
            user_id (int): The ID of the user to check.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        self.logger.debug(f"Checking if user exists: {user_id}")
        user = self.get_user(user_id)
        return user is not None
            

    def add_user(self, user_id, is_admin):
        """
        Adds a new user to the database.

        Args:
            user_id (str): The ID of the user.
            is_admin (bool): Indicates whether the user is an admin or not.

        Returns:
            bool: True if the user was successfully added, False if the user already exists.
        """
        self.logger.info(f"Adding new user: {user_id}")
        does_user_exist = self.check_for_user(user_id)
        if does_user_exist:
            return False

        new_user = User(user_id=user_id, is_admin=is_admin)
        with self.get_db() as session:
            session.add(new_user)
            session.commit()

    def get_user(self, user_id):
        """
        Retrieve a user from the database based on the provided user ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User: The user object corresponding to the provided user ID, or None if no user is found.
        """
        self.logger.debug(f"Getting user: {user_id}")
        with self.get_db() as session:
            user = session.query(User).filter(User.user_id == user_id).first()

        return user

    def get_all_users(self):
        """
        Retrieve all users from the database.

        Returns:
            list: A list of User objects representing all the users in the database.
        """
        self.logger.debug(f"Getting all users")
        with self.get_db() as session:
            users = session.query(User).all()
        
        return users

    def update_user(self, user_id, is_admin=None):
        """
        Update the user's admin status.

        Args:
            user_id (int): The ID of the user to update.
            is_admin (bool, optional): The new admin status of the user. Defaults to None.

        Returns:
            None
        """
        self.logger.info(f"Updating user: {user_id}")
        with self.get_db() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                if is_admin is not None:
                    user.is_admin = is_admin
                session.commit()


    def delete_user(self, user_id):
        """
        Deletes a user from the database.

        Args:
            user_id (int): The ID of the user to be deleted.

        Returns:
            None
        """
        self.logger.info(f"Deleting user: {user_id}")
        with self.get_db() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                session.delete(user)
                session.commit()

    def get_number_of_asked_questions(self, given_timestamp): 
        """
        Get the number of asked questions from the database.

        Args:
            given_timestamp (datetime): The timestamp to filter the search history.

        Returns:
            int: The number of asked questions.

        """
        self.logger.debug(f"Getting number of asked questions")
        with self.get_db() as session:
            number_of_asked_questions = session.query(SearchHistory).filter(
                SearchHistory.timestamp <= datetime.utcnow(),
                SearchHistory.timestamp >= given_timestamp).count()
            
        return number_of_asked_questions

    def get_search_history(self, user_id):
        """
        Retrieves the search history for a given user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list: A list of SearchHistory objects representing the search history.
        """
        self.logger.debug(f"Getting search history for user: {user_id}")
        with self.get_db() as session:
            history = session.query(SearchHistory).filter(SearchHistory.user_id == user_id).order_by(
            SearchHistory.timestamp.desc()).all()
        return history

    def log_search(self, user_id, query):
        """
        Logs a search query for a user in the database.

        Args:
            user_id (int): The ID of the user performing the search.
            query (str): The search query.
            session (Session, optional): The database session. If not provided, a new session will be created.

        Returns:
            None
        """
        self.logger.debug(f"Saving search for user {user_id}: {query}")
        with self.get_db() as session:
            try:
                
                # Check if max history count reached
                current_history_count = session.query(SearchHistory).filter(SearchHistory.user_id == user_id).count()
                if current_history_count >= config.max_search_history_per_user:
                    # Delete the oldest entry
                    oldest_entry = session.query(SearchHistory).filter(SearchHistory.user_id == user_id).order_by(
                        SearchHistory.timestamp.asc()).first()
                    session.delete(oldest_entry)

                # Add new search history
                new_search_history = SearchHistory(user_id=user_id, search_query=query)
                session.add(new_search_history)
                session.commit()
            except Exception as e:
                # print(f"Error in log_search: {e}")
                self.logger.error(f"Error in log_search: {e}")
                session.rollback()

    def get_admin_settings(self):
        """
        Retrieve the admin settings from the database.

        Returns:
            AdminSettings: The admin settings object.
        """
        self.logger.debug("Fetching admin settings")
        with self.get_db() as session:
            settings = session.query(AdminSettings).first()
        return settings

    def update_admin_settings(self, logout_timer=None, max_disk_space=None, user_max_disk_space=None):
        """
        Update the admin settings in the database.

        Args:
            logout_timer (int, optional): The logout timer value in seconds. Defaults to None.
            max_disk_space (int, optional): The maximum disk space value in bytes. Defaults to None.
            user_max_disk_space (int, optional): The maximum disk space value per user in bytes. Defaults to None.
        """
        self.logger.info("Updating admin settings")

        with self.get_db() as session:
            settings = session.query(AdminSettings).first()
            if not settings:
                settings = AdminSettings()
                session.add(settings)
            if logout_timer is not None:
                settings.logout_timer = logout_timer
            if max_disk_space is not None:
                settings.max_disk_space = max_disk_space
            if user_max_disk_space is not None:
                settings.user_max_disk_space = user_max_disk_space
            session.commit()

    def update_last_login(self, user_id):
        """
        Update the last login time for a user.

        :param user_id: ID of the user who logged in
        """
        with self.get_db() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                current_datetime  = datetime.now()
                # Eine Stunde hinzufügen
                updated_last_login = current_datetime + timedelta(hours=1)

                user.last_login = updated_last_login
                session.commit()


    def get_active_users(self):
        """
        Retrieve a list of active users.

        :return: List of active users
        """
        thirty_days_ago = datetime.now() - timedelta(days=30)
        with self.get_db() as session:
            active_users_count = session.query(User).filter(User.last_login >= thirty_days_ago).count()
        return active_users_count

    def get_inactive_users(self):
        """
        Retrieve a list of inactive users.

        :return: List of inactive users
        """
        thirty_days_ago = datetime.now() - timedelta(days=30)
        with self.get_db() as session:
            inactive_users_count = session.query(User).filter(User.last_login < thirty_days_ago).count()
        return inactive_users_count
    








