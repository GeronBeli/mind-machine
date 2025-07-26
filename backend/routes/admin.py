from fastapi.responses import FileResponse
from dependencies import fs_dependency, user_dependency
from fastapi import APIRouter, HTTPException, status
from services.admin_settings_service import get_settings, update_settings
from services.user_service import get_active_users_count, get_all_users
from services.search_service import get_searches_list
import logging
from database import DbSession

admin_router = APIRouter(tags=['admin'])


def check_admin_authorization(user: user_dependency):
        """
        Checks if the user is authenticated and an admin.
        
        Args:
        user: The user object to check.

        Raises:
        HTTPException: If the user is not authenticated or not an admin.
        """
        if not user:
            logging.error("User authentication failed")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Authentication failed"
            )
        
        if not user.get('is_admin'):
            logging.error("User is not authorized to access admin resources")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="You do not have permission to access this resource"
            )
        


@admin_router.get("/diskusage", status_code=status.HTTP_200_OK)
async def get_disk_usage(db: DbSession, admin: user_dependency, fs: fs_dependency):
    check_admin_authorization(admin)
    disk_usage = get_settings(db).max_disk_space
    disk_usage = fs.convert_bytes_to_gigabyte(disk_usage)
    return disk_usage

@admin_router.put("/diskusage", status_code=status.HTTP_204_NO_CONTENT)
async def change_disk_usage(db: DbSession, admin: user_dependency, disk_usage: float):
    check_admin_authorization(admin)
    update_settings(db, max_disk_space=disk_usage)

@admin_router.put("/diskusage/user", status_code=status.HTTP_204_NO_CONTENT)
async def change_disk_usage(db: DbSession, admin: user_dependency, disk_usage: float):
    check_admin_authorization(admin)
    update_settings(db, user_max_disk_space=disk_usage)
    return True

@admin_router.get("/storage_usage", status_code=status.HTTP_200_OK)
async def get_storage_info(admin: user_dependency, fs: fs_dependency):
    check_admin_authorization(admin)
    total_size = fs.get_total_file_size_for_all_users()
    return total_size

@admin_router.get("/storage_usage/{user_id}", status_code=status.HTTP_200_OK)
async def get_storage_info(admin: user_dependency, fs: fs_dependency, user_id):
    check_admin_authorization(admin)
    total_size = fs.get_file_size_for_user(user_id)
    return total_size

@admin_router.get("/statistics", status_code=status.HTTP_200_OK)
async def get_statistics(db: DbSession, admin: user_dependency, fs: fs_dependency):
    check_admin_authorization(admin)
    activeUsers = get_active_users_count(db)
    statistics = get_all_users(db)

    for user in statistics:
        user.used_storage = fs.get_file_size_for_user(user.user_id)
        
    return {"statistics": statistics, "activeUsers": activeUsers}


@admin_router.put("/autologout",status_code=status.HTTP_204_NO_CONTENT)
async def set_auto_logout(db: DbSession, admin: user_dependency, logout_timer: float):
    check_admin_authorization(admin)
    update_settings(db, logout_timer=logout_timer)
    return True

@admin_router.get("/getnumberofaskedquestions", status_code=status.HTTP_200_OK)
async def get_number_of_asked_questions(db: DbSession, admin: user_dependency):
    check_admin_authorization(admin)
    number_of_questions = get_searches_list(db)
    return {"number_of_questions": number_of_questions}


# @admin_router.get("/logfile", status_code=status.HTTP_200_OK)
# async def get_log_file(admin: user_dependency):
#     check_admin_authorization(admin)
#     return FileResponse(=get_log_file_as_json(), filename="log.txt", media_type="text/plain")