
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from CRUD import contacts

from DB import database, schemas


router = APIRouter(prefix='/contacts',
                   tags=['Contacts'])


# Get all contacts
@router.get("/read/all", response_model=list[schemas.Contacts])
async def read_contacts(skip: int = 0, limit: int = 50, db: Session = Depends(database.get_db)):

    all_contacts = contacts.get_all_contacts(db)

    if all_contacts:
        return all_contacts

    raise HTTPException(
        status_code=400,
        detail="Database is empty"
    )


# Get a contact by it's ID
@router.get("/read/id/{contact_id}", response_model=schemas.Contacts)
async def read_contact_by_id(contact_id: int, db: Session = Depends(database.get_db)):

    # Check if exists that contact
    db_contact = contacts.get_contact_by_id(contact_id=contact_id, db=db)
    if db_contact:

        return db_contact

    raise HTTPException(status_code=404, detail="Contact not found.")


# Get a contact by it's phone
@router.get("/read/phone/{contact_phone}", response_model=schemas.Contacts)
async def read_contact_by_phone(contact_phone: str, db: Session = Depends(database.get_db)):

    # Check if exists that contact
    db_contact = contacts.get_contact_by_phone(contact_phone=contact_phone, db=db)
    if db_contact:

        return db_contact

    raise HTTPException(status_code=404, detail="Contact not found.")


# Create a new contact
@router.post("/create", response_model=schemas.Contacts)
async def create_new_contact(contact: schemas.ContactsCreate, db: Session = Depends(database.get_db)):

    new_contact = contacts.create_contact(contact=contact, db=db)

    if new_contact:
        return new_contact

    raise HTTPException(
        status_code=400,
        detail="Could not create a new contact."
    )


# Delete a contact
@router.delete("/delete/{contact_id}", response_model=schemas.Contacts)
def delete_contact_by_id(contact_id: int, db: Session = Depends(database.get_db)):

    # Check if exists that contact
    db_contact = contacts.get_contact_by_id(contact_id=contact_id, db=db)
    if db_contact:

        db_contact = contacts.delete_contact(contact_id=contact_id, db=db)
        return db_contact

    raise HTTPException(status_code=404, detail="Contact not found.")


# Update a new contact
@router.put("/update/{contact_id}", response_model=schemas.Contacts)
async def update_contact_by_id(contact: schemas.ContactsCreate, contact_id: int, db: Session = Depends(database.get_db)):

    # Check if exists that contact
    db_contact = contacts.get_contact_by_id(contact_id=contact_id, db=db)

    if db_contact:
        updated_db = contacts.update_contact(db_contact=db_contact, contact=contact, db=db)

        return updated_db

    raise HTTPException(
        status_code=400,
        detail="Could not update contact."
    )
