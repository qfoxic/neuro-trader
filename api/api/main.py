from fastapi import FastAPI
from .routes.main import router

app = FastAPI()

@app.get("/", tags=["Root"])
async def read_root():
  return {
    "message": "Welcome to my notes application, use the /docs route to proceed"
  }

app.include_router(router, prefix="/v1")

