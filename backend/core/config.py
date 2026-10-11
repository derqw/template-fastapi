from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

class AuthJWT(BaseModel):
    private_key_path : Path = BASE_DIR /'secrets' / 'private.pem'
    public_key_path : Path = BASE_DIR / 'secrets' / 'public.pem'
    algorithm : str = 'RS256'
    access_token_expire_minutes : int = 60
    refresh_token_expire_day : int = 30

class Database(BaseSettings):
    DB_USER : str
    DB_PASSWORD : str 
    DB_HOST : str
    DB_PORT : str
    DB_NAME : str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def DATABASE_URL(self):
        return  f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    

class Settings(BaseSettings):
    app_name = 'book-test'

    static_dir : str =  "static"
    image_url : str = "static/image"

    auth_jwt : AuthJWT = AuthJWT()

    db : Database = Field(default_factory=Database)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        extra="ignore"
    )

settings = Settings()