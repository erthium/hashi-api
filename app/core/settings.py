from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
  PROJECT_NAME: str = "Hashi API"
  DESCRIPTION: str = "RestAPI of the Hashiwokakero puzzle"
  VERSION: str = "0.0.1"

  DATABASE_URL: str = os.environ.get("DATABASE_URL")
  DEVELOPMENT: bool = os.environ.get("DEVELOPMENT", 0) == 1
  LOCK_DB_WRITE: bool = os.environ.get("LOCK_DB_WRITE", 0) == 1
  PORT: int = os.environ.get("PORT", 8000)

settings = Settings()
