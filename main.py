"""
Main file to start.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import uvicorn

import app
from app.raspi_functions import cleanup
from app.router import main_router


# Initialize FastAPI
app = FastAPI(title='ROBOKOS')
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(main_router)


if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port=8030)
    finally:
        cleanup()
