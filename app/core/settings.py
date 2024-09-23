from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
  PROJECT_NAME: str = "Hashi API"
  DESCRIPTION: str = "RestAPI of the Hashiwokakero puzzle"
  VERSION: str = "0.0.1"

  DATABASE_URL: str = os.environ.get("DATABASE_URL")
  PORT: int = os.environ.get("PORT", 8000)

settings = Settings()
