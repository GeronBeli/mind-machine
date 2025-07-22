import logging
from typing import List
from repositories import SearchRepository
from models import SearchHistory
from datetime import datetime, timezone
import config


logger = logging.getLogger(__name__)

class SearchService:
    """Service for handling search history operations."""
    
    def __init__(self, search_repository: SearchRepository):
        self.logger = logger
        self.search_repository = search_repository
    
    def get_search_history(self, user_id: str) -> List[SearchHistory]:
        """
        Retrieve search history for a user.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            List of SearchHistory objects for the user
        """
        try:
            self.logger.debug(f"Getting search history for user: {user_id}")
            return self.search_repository.get_search_history(user_id)
        except Exception as e:
            self.logger.error(f"Error getting search history for user {user_id}: {e}")
            return []
    
    def log_search(self, user_id: str, query: str):
        """
        Log a search query for a user.
        
        Args:
            user_id: The ID of the user performing the search
            query: The search query string
            
        Returns:
            True if search was logged successfully, False otherwise
        """
        try:
            self.logger.debug(f"Logging search for user {user_id}: {query}")
            
            # Check if we need to delete oldest search to maintain limit
            history_count = len(self.search_repository.get_search_history(user_id))
            if history_count >= config.max_search_history_per_user:
                self.search_repository.delete_oldest_search(user_id)
            
            # Create new search history entry
            search_history = SearchHistory(
                user_id=user_id, 
                search_query=query,
                timestamp=datetime.now(timezone.utc)
            )
            
            self.search_repository.add_search(search_history)
            
        except Exception as e:
            self.logger.error(f"Error logging search for user {user_id}: {e}")
    

