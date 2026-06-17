import os
from typing import Optional

class Settings:
    PROJECT_NAME: str = "车辆调度与维保系统"
    VERSION: str = "1.0.0"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "vehicle-secret-key-2024")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://vehicle_user:vehicle_pass@localhost/vehicle_db?charset=utf8mb4"
    )

settings = Settings()
