from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import generator
#from app.routers import storage
#from app.core.config import settings

import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

app.include_router(generator.router, prefix="/hashi/generator")
#app.include_router(storage.router, prefix="/hashi/storage")

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

@app.get("/")
def get_root():
  return {"V"} # V for Vendetta


if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=os.environ.get("PORT", 8000))
