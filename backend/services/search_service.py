import logging
from typing import List
from models import SearchHistory
from datetime import datetime, timezone
import config
from database import DbSession
import logging

    
def get_searches_list(db: DbSession, user_id: str) -> List[SearchHistory]:
    """
    Retrieve search history for a user.
    
    Args:
        user_id: The ID of the user
        
    Returns:
        List of SearchHistory objects for the user
    """
    try:
        logging.debug(f"Getting search history for user: {user_id}")
        return db.query(SearchHistory).filter(SearchHistory.user_id == user_id).order_by(SearchHistory.timestamp.desc())\
            .all()
    except Exception as e:
        logging.error(f"Error getting search history for user {user_id}: {e}")
        return []


def log_search(db: DbSession, user_id: str, query: str):
    """
    Log a search query for a user.
    
    Args:
        user_id: The ID of the user performing the search
        query: The search query string
        
    Returns:
        True if search was logged successfully, False otherwise
    """
    try:
        # Check if we need to delete oldest search to maintain limit
        history_count = len(get_searches_list(db, user_id))
        if history_count >= config.max_search_history_per_user:
            delete_oldest_search(db, user_id)
        
        # Create new search history entry
        search_history = SearchHistory(
            user_id=user_id, 
            search_query=query,
            timestamp=datetime.now(timezone.utc)
        )
        
        db.add(search_history)
        db.commit()
        logging.debug(f"Logging search for user {user_id}: {query}")
        
    except Exception as e:
        logging.error(f"Error logging search for user {user_id}: {e}")


def delete_oldest_search(db: DbSession, user_id):
    oldest = (db.query(SearchHistory)
                .filter(SearchHistory.user_id == user_id)
                .order_by(SearchHistory.timestamp.asc())
                .first())
    if oldest:
        db.delete(oldest)
        db.commit()


