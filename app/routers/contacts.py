
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from CRUD import contacts

from DB import database, schemas

from datetime import date
from loguru import logger


router = APIRouter(prefix='/contacts',
                   tags=['Contacts'])


# Log File
today = date.today().strftime("%b-%d-%Y")
logger.add(f"logs/contacts_log_{today}.log")


# Get all contacts
@router.get("/read/all", response_model=list[schemas.Contacts])
async def read_contacts(skip: int = 0, limit: int = 50, db: Session = Depends(database.get_db)):

    all_contacts = contacts.get_all_contacts(db)

    if all_contacts:
        logger.info("Read all contacts of database.")
        return all_contacts

    logger.warning("No contacts in database.")
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

        logger.info(f"Read contact with id {contact_id}.")
        return db_contact

    logger.warning(f"No contact with id {contact_id} in database.")
    raise HTTPException(status_code=404, detail="Contact not found.")


# Get a contact by it's phone
@router.get("/read/phone/{contact_phone}", response_model=schemas.Contacts)
async def read_contact_by_phone(contact_phone: str, db: Session = Depends(database.get_db)):

    # Check if exists that contact
    db_contact = contacts.get_contact_by_phone(contact_phone=contact_phone, db=db)
    if db_contact:

        logger.info(f"Read contact with phone {contact_phone}.")
        return db_contact

    logger.warning(f"No contact with phone {contact_phone} in database.")
    raise HTTPException(status_code=404, detail="Contact not found.")


# Create a new contact
@router.post("/create", response_model=schemas.Contacts)
async def create_new_contact(contact: schemas.ContactsCreate, db: Session = Depends(database.get_db)):

    new_contact = contacts.create_contact(contact=contact, db=db)

    if new_contact:

        logger.success(f"New contact created with success!")
        return new_contact

    logger.error(f"Could not create a new contact.")
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
        logger.success(f"Contact with id {contact_id} deleted with success!")
        return db_contact

    logger.error(f"Could not delete contact with id {contact_id}.")
    raise HTTPException(status_code=404, detail="Contact not found.")


# Update a new contact
@router.put("/update/{contact_id}", response_model=schemas.Contacts)
async def update_contact_by_id(contact: schemas.ContactsCreate, contact_id: int, db: Session = Depends(database.get_db)):

    # Check if exists that contact
    db_contact = contacts.get_contact_by_id(contact_id=contact_id, db=db)

    if db_contact:
        updated_db = contacts.update_contact(db_contact=db_contact, contact=contact, db=db)

        logger.success(f"Contact with id {contact_id} updated with success!")
        return updated_db

    logger.error(f"Could not update contact with id {contact_id}.")
    raise HTTPException(
        status_code=400,
        detail="Could not update contact."
    )
