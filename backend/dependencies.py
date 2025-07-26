from fastapi import Depends
from utils.neural_search.qdrant import Qdrant
from utils.file_sys import FileSystemHandler
from services.auth_service import get_current_user
from typing import Annotated

def get_qd_client() -> Qdrant:
    """
    Dependency to get the Qdrant client.
    """
    return Qdrant()
Qdrant_dependency = Annotated[Qdrant, Depends(get_qd_client)]


def get_file_system_handler(qd: Qdrant_dependency) -> FileSystemHandler:
    """
    Dependency to get the FileSystemHandler.
    """
    return FileSystemHandler(qd)

fs_dependency = Annotated[FileSystemHandler, Depends(get_file_system_handler)]

user_dependency = Annotated[dict, Depends(get_current_user)]