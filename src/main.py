import subprocess
from multiprocessing import Process

from fastapi import FastAPI
import uvicorn

from src.infrastructure.db.mongo_db.mongo_connection import init_db
from src.infrastructure.rest_api.routers.parsing_routers import parsing_router

app = FastAPI()

app.include_router(parsing_router)

init_db()

def start_uvicorn():
    uvicorn.run("main:app", host="0.0.0.0", port=8035, workers=1)

def start_celery_worker():
    subprocess.run([
        "celery",
        "-A", "src.services.celery_worker.celery_worker",
        "worker",
        "--loglevel=info"
    ])

if __name__ == "__main__":
    process1 = Process(target=start_uvicorn)
    process2 = Process(target=start_celery_worker)

    process1.start()
    process2.start()

    process1.join()
    process2.join()