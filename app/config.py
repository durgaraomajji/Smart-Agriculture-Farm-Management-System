from pydantic import BaseModel


class Settings(BaseModel):
    DATABASE_URL: str = "mysql+pymysql://root:Root123@localhost:3306/smart_agriculture"
    SECRET_KEY: str = "smart-agriculture-change-this-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


settings = Settings()