
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from CRUD import contacts
from DB import database, schemas

from loguru import logger


router = APIRouter(tags=['HTML Pages'])


templates = Jinja2Templates(directory="templates")


# Home Page
@router.get("/", response_class=HTMLResponse)
async def index(request: Request):

    return templates.TemplateResponse("index.html", {"request": request})


# Contacts
@router.get("/contatos", response_class=HTMLResponse)
async def contatos(request: Request):

    return templates.TemplateResponse("contacts.html", {"request": request})


# Read All Contacts
@router.get("/contatos/all", response_class=HTMLResponse)
async def contatos_read_all(request: Request, db: Session = Depends(database.get_db)):

    all_contacts = contacts.get_all_contacts(db)

    if all_contacts:
        logger.info("Read all contacts of database.")
        return templates.TemplateResponse("contacts.html", {"request": request, "all_contacts": all_contacts})

    logger.warning("No contacts in database.")
    raise HTTPException(
        status_code=400,
        detail="Database is empty"
    )


# Read contact by it's ID
@router.get("/contatos/id", response_class=HTMLResponse)
async def contatos_read_by_id(request: Request, contact_id: int, db: Session = Depends(database.get_db)):

    # Check if exists that contact
    db_contact = contacts.get_contact_by_id(contact_id=contact_id, db=db)
    if db_contact:

        logger.info(f"Read contact with id {contact_id}.")
        return templates.TemplateResponse("contacts.html", {"request": request, "search_id": db_contact})

    logger.warning(f"No contact with id {contact_id} in database.")
    return templates.TemplateResponse("contacts.html", {"request": request, "error": f"No contact with id {contact_id} in database."})


# Delete contact by it's ID
@router.get("/contatos/delete", response_class=HTMLResponse)
async def contatos_delete_by_id(request: Request, contact_id: int, db: Session = Depends(database.get_db)):

    # Check if exists that contact
    db_contact = contacts.get_contact_by_id(contact_id=contact_id, db=db)
    if db_contact:

        db_contact = contacts.delete_contact(contact_id=contact_id, db=db)
        logger.success(f"Contact with id {contact_id} deleted with success!")
        return templates.TemplateResponse("contacts.html", {"request": request, "delete_msg": f"Contact with id {contact_id} deleted with success!"})

    logger.error(f"Could not delete contact with id {contact_id}.")
    return templates.TemplateResponse("contacts.html", {"request": request, "error": f"No contact with id {contact_id} in database."})


# Developer
@router.get("/desenvolvedor", response_class=HTMLResponse)
async def desenvolvedor(request: Request):

    return templates.TemplateResponse("developer.html", {"request": request})
