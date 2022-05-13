
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from CRUD import contacts

from DB import database, schemas


router = APIRouter(prefix='/contacts',
                   tags=['Contacts'])


# Get all contacts
@router.get("/all")
async def read_contacts(db: Session = Depends(database.get_db)):

    all_contacts = contacts.get_all_contacts(db)

    if all_contacts:
        return all_contacts

    raise HTTPException(
        status_code=400,
        detail="Database is empty"
    )


# Create a new contact
@router.post("/create", response_model=schemas.Contacts)
async def create_new_contact(contact: schemas.ContactsCreate, db: Session = Depends(database.get_db)):

    new_contact = contacts.create_contact(contact=contact, db=db)

    if new_contact:
        return new_contact

    raise HTTPException(
        status_code=400,
        detail="Database is empty"
    )
