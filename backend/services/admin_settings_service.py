from models import AdminSettings
import config
from database import DbSession


def get_settings(db: DbSession) -> AdminSettings:
    settings = db.query(AdminSettings).first()
    if not settings:
        settings = init_settings(db)
    return settings

def init_settings(db: DbSession):
    settings = db.query(AdminSettings).first()
    if settings:
        return settings

    new_settings = AdminSettings(
        logout_timer=config.logout_timer,
        max_disk_space=config.max_disk_space,
        user_max_disk_space=config.user_max_disk_space
    )
    db.add(new_settings)
    db.commit()
    return new_settings

def update_settings(db: DbSession, logout_timer=None, max_disk_space=None, user_max_disk_space=None):
    settings = db.query(AdminSettings).first()
    if not settings:
        settings = AdminSettings()
        db.add(settings)
    if logout_timer is not None:
        settings.logout_timer = logout_timer
    if max_disk_space is not None:
        settings.max_disk_space = max_disk_space
    if user_max_disk_space is not None:
        settings.user_max_disk_space = user_max_disk_space
    db.commit()
            
