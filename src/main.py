import logging
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import general_settings
from routes import router

curr_workspace = os.getcwd()
parent_dir = os.path.dirname(curr_workspace)

root_logger = logging.getLogger()
file_handler = logging.FileHandler(f"{parent_dir}/anime-scraper.log")
file_handler.setFormatter(
    logging.Formatter(
        fmt="%(name)s | %(levelname)s | %(asctime)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )
)
root_logger.setLevel(logging.INFO)
root_logger.addHandler(file_handler)

app = FastAPI(
    title="Anime Scraper API",
    description="Scraper for anime data and download links.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


if __name__ == "__main__":
    HOST = general_settings.HOST
    PORT = general_settings.PORT
    DEBUG = general_settings.DEBUG
    APP_NAME = general_settings.APP_NAME
    uvicorn.run(app=APP_NAME, host=HOST, port=PORT, reload=DEBUG)
