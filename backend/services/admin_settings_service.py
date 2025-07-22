from repositories import AdminRepository
from models import AdminSettings
import config
from logHandler import LogHandler
from sqlalchemy.orm import Session

class AdminSettingsService:
    def __init__(self, db: Session):
        self.logger = LogHandler(name="AdminSettingsService").get_logger()
        self.db = db
        self.init_settings()

    def get_settings(self):
        settings = self.db.query(AdminSettings).first()
        if not settings:
            raise ValueError("Admin settings not initialized")
        return settings

    def init_settings(self):
        settings = self.db.query(AdminSettings).first()
        if settings:
            return settings

        new_settings = AdminSettings(
            logout_timer=config.logout_timer,
            max_disk_space=config.max_disk_space,
            user_max_disk_space=config.user_max_disk_space
        )
        self.db.add(new_settings)
        self.db.commit()
        return new_settings

    def update_settings(self, logout_timer=None, max_disk_space=None, user_max_disk_space=None):
        settings = self.db.query(AdminSettings).first()
        if not settings:
            settings = AdminSettings()
            self.db.add(settings)
        if logout_timer is not None:
            settings.logout_timer = logout_timer
        if max_disk_space is not None:
            settings.max_disk_space = max_disk_space
        if user_max_disk_space is not None:
            settings.user_max_disk_space = user_max_disk_space
        self.db.commit()
