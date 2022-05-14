
from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from DB import models
from DB.database import engine

from routers import contacts
from routers import html_pages


# Create tables
models.Base.metadata.create_all(bind=engine)

# Instance of FastAPI
app = FastAPI()


# Configuration of static folders
app.mount("/static", StaticFiles(directory="static"), name="static")


# ROUTERS
app.include_router(contacts.router)
app.include_router(html_pages.router)
