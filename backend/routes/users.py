from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from services.admin_settings_service import get_settings
from fastapi import status
from services.search_service import log_search, get_searches_list
from schemas import RenameFileModel  
from dependencies import Qdrant_dependency, fs_dependency, user_dependency
import logging
from database import DbSession

user_router = APIRouter(tags=['user'])



def check_user_authentication(user: user_dependency):
        """
        Checks if the user is authenticated.
        
        Args:
        user: The user object to check.

        Raises:
        HTTPException: If the user is not authenticated.
        """
        if not user:
            logging.error("User authentication failed")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Authentication failed"
            )
        


@user_router.get("/search", status_code=status.HTTP_200_OK)
async def search(db: DbSession, user: user_dependency, qd: Qdrant_dependency, query: str):
    check_user_authentication(user)
    try:
        # Perform the search using Qdrant
        results = qd.search(user.get('user_id'), query)
        log_search(db, user.get('user_id'), query) 
        logging.info(f"User {user.get('user_id')} searched for {query}")
        return results
    except Exception as e:
        logging.info(f"User {user.get('user_id')} failed to search for {query}")
        raise HTTPException(status_code=500, detail=str(e))
    

@user_router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(user: user_dependency, fs: fs_dependency,files: list[UploadFile] = File(...)):
    check_user_authentication(user)
    status_return = fs.upload(user.get('user_id'), files)
    logging.info(f"User {user.get('user_id')} uploaded {len(files)} files: {status_return}")
    return status_return


@user_router.get("/document",status_code=status.HTTP_200_OK)
async def get_document(user: user_dependency, fs: fs_dependency, document_name :str):  # (user_id: str, document_name: str):
    check_user_authentication(user)
    filepath = fs.get_document_path(user.get('user_id'), document_name)
    if not filepath:
        logging.error(f"User {user.get('user_id')} failed to download {document_name}")
        raise HTTPException(status_code=404, detail="File not found")
    logging.info(f"User {user.get('user_id')} downloaded {document_name}")
    return FileResponse(path=filepath, filename=document_name, media_type="application/pdf")


@user_router.delete("/deleteDocument/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(user: user_dependency, fs: fs_dependency, document_id: str):
    check_user_authentication(user)
    logging.info(f"User {user.get('user_id')} deleted {document_id}")
    fs.delete_document(user.get('user_id'), document_id)
    return True


@user_router.get("/filestructure", status_code=status.HTTP_200_OK)
async def get_file_structure(user: user_dependency, fs: fs_dependency):
    check_user_authentication(user)
    logging.info(f"User {user.get('user_id')} requested file structure")
    return fs.get_fs_for_user(user.get('user_id'))


@user_router.put("/editDocumentName", status_code=status.HTTP_204_NO_CONTENT)
async def edit_document_name(user: user_dependency, fs: fs_dependency,
    qd: Qdrant_dependency, request: RenameFileModel):
    check_user_authentication(user)
    fs.edit_document_name(user.get('user_id'), request.old_name, request.new_name)
    qd.rename_doc(user.get('user_id'), request.old_name, request.new_name)
    logging.info(f"User {user.get('user_id')} renamed {request.old_name} to {request.new_name}")
    return True

@user_router.head("/revectorize", status_code=status.HTTP_200_OK)
async def revectorize(user: user_dependency, qd: Qdrant_dependency):
    check_user_authentication(user)
    qd.revectorize_all()
    logging.info(f"User {user.get('user_id')} revectorized all documents")
    return True

@user_router.get("/current_storage_usage", status_code=status.HTTP_200_OK)
async def get_storage_info(user: user_dependency,fs: fs_dependency):
    check_user_authentication(user)
    total_size = fs.get_file_size_for_user(user.get('user_id'), inBytes=True)
    return total_size

@user_router.get("/searchhistory", status_code=status.HTTP_200_OK)
async def get_search_history(db: DbSession, user: user_dependency):
    check_user_authentication(user)
    raw_search_history = get_searches_list(db, user.get('user_id'))
    search_history = []
    for search in raw_search_history:
        search_history.append({'query': search.search_query, 'date': search.timestamp})
    return search_history

@user_router.get("/diskusage/user", status_code=status.HTTP_200_OK)
async def get_disk_usage(db: DbSession, user: user_dependency, fs: fs_dependency, inBytes: str):
    check_user_authentication(user)
    disk_usage = get_settings(db).user_max_disk_space
    if inBytes == "false":
        disk_usage = fs.convert_bytes_to_gigabyte(disk_usage)
    return disk_usage

@user_router.get("/autologout", status_code=status.HTTP_200_OK)
async def get_auto_logout(db: DbSession, user: user_dependency):
    check_user_authentication(user)
    settings = get_settings(db).logout_timer
    return settings