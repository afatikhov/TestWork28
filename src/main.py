from fastapi import FastAPI
import uvicorn

from src.infrastructure.db.mongo_db.mongo_connection import init_db
from src.infrastructure.rest_api.routers.parsing_routers import parsing_router

app = FastAPI()

app.include_router(parsing_router)

init_db()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8035, workers=1)