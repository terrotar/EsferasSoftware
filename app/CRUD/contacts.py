
from sqlalchemy.orm import Session

from DB import models, schemas

from typing import Optional

from validate_docbr import CPF

from email_validator import validate_email, EmailNotValidError, caching_resolver

from fastapi import HTTPException


# Instance of CPF checker
cpf = CPF()


# Set a timeout for email checker
resolver = caching_resolver(timeout=10)


# Cpf Checker
def check_cpf(doc):

    try:
        doc = cpf.mask(doc)
        checker = cpf.validate(doc)

        if checker is True:
            return checker

        return False

    except Exception:
        return False


# Email Checker
def check_email(email):

    try:
        checker = validate_email(email, dns_resolver=resolver).email

        if checker:
            return True

        return False

    except EmailNotValidError:
        return False

    except Exception:
        return False


# Read Contacts
def get_all_contacts(db: Session):
    all_contacts = db.query(models.Contacts).all()
    return all_contacts


# Create Contact
def create_contact(contact: schemas.ContactsCreate, db: Session):

    # CPF and Email Checkers
    cpf_checker = check_cpf(contact.cpf)
    email_checker = check_email(contact.email)
    if(cpf_checker is True and email_checker is True):

        # Checks if a contact's already in database
        check_contact = db.query(models.Contacts).filter(
            models.Contacts.name == contact.name).first()
        if(not check_contact):

            # Add new contact in database
            new_contact = models.Contacts(name=contact.name,
                                          last_name=contact.last_name,
                                          phone=contact.phone,
                                          cpf=contact.cpf,
                                          email=contact.email)
            db.add(new_contact)
            db.commit()
            db.refresh(new_contact)

            return new_contact

        else:
            raise HTTPException(
                status_code=400,
                detail="Contact already exists."
            )

    else:
        raise HTTPException(
                status_code=400,
                detail="CPF or Email invalid."
            )
