
from fastapi import FastAPI

from DB import models
from DB.database import engine

from routers import contacts


# Create tables
models.Base.metadata.create_all(bind=engine)

# Instance of FastAPI
app = FastAPI()


# ROUTERS

# Contacts
app.include_router(contacts.router)
