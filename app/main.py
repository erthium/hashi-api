import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import engine
from app.routers import storage
from app.core.settings import settings

# Ensure app logs are visible under uvicorn (which leaves the root logger
# without an INFO handler).
logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

app = FastAPI()

app.include_router(engine.router, prefix="/hashi/engine")
app.include_router(storage.router, prefix="/hashi/storage")

origins = [
  "http://localhost",
  "http://localhost:8000",
  "http://localhost:5000",
  "https://erthium.tech",
  "https://www.erthium.tech",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.get(
  "/",
  summary="Root",
  description="Root endpoint",
  response_description="Beneath this mask, there is more than flesh...",
)
def get_root():
  return "V" # V for Vendetta


if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
