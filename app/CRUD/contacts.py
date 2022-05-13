
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

        doc = cpf.mask(str(doc))
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


# Read Contactg by it's ID
def get_contact_by_id(contact_id: int, db: Session):

    db_contact = db.query(models.Contacts).filter(
        models.Contacts.id == contact_id).first()

    return db_contact


# Create Contact
def create_contact(contact: schemas.ContactsCreate, db: Session):

    try:

        # Validate size of phone number
        phone_checker = len(str(contact.phone))
        if(8 <= phone_checker <= 14):

            # CPF and Email Checkers
            cpf_checker = check_cpf(contact.cpf)
            email_checker = check_email(contact.email)
            # print(cpf_checker, email_checker)

            if(cpf_checker is True and email_checker is True):

                # Add new contact in database
                new_contact = models.Contacts(name=contact.name,
                                              last_name=contact.last_name,
                                              phone=f"{contact.phone};",
                                              cpf=contact.cpf,
                                              email=f"{contact.email};")
                db.add(new_contact)
                db.commit()
                db.refresh(new_contact)

                return new_contact

            else:
                raise NameError

        else:
            raise ValueError

    except NameError:
        raise HTTPException(
            status_code=400,
            detail="CPF or Email invalid."
        )

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Phone must be between 8 and 14 digits."
        )

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Contact already exists."
        )


# Delete a contact by it's ID
def delete_contact(contact_id: int, db: Session):
    db_contact = db.query(models.Contacts).filter(models.Contacts.id == contact_id).first()
    db.delete(db_contact)
    db.commit()
    return db_contact
