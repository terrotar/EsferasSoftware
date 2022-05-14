
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from CRUD import contacts
from DB import database


router = APIRouter(tags=['HTML Pages'])


templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(database.get_db)):

    all_contacts = contacts.get_all_contacts(db)

    return templates.TemplateResponse("index.html", {"request": request, "all_contacts": all_contacts})
