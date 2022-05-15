
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
async def index(request: Request):

    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/contatos", response_class=HTMLResponse)
async def contatos(request: Request):

    return templates.TemplateResponse("contacts.html", {"request": request})


@router.get("/desenvolvedor", response_class=HTMLResponse)
async def desenvolvedor(request: Request):

    return templates.TemplateResponse("developer.html", {"request": request})
