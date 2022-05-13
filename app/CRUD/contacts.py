
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


# Phone Checker
def check_phone(contact: schemas.ContactsBase):

    try:

        checker = []
        contact_phones = [contact.phone_01, contact.phone_02, contact.phone_03]

        for i in range(0, len(contact_phones)):

            if contact_phones[i] != "string" and contact_phones[i] != "":

                phone_checker = len(str(contact_phones[i]))

                if phone_checker >= 8:
                    checker.append(True)

                else:
                    checker.append(False)

            else:
                checker.append(True)

        return checker

    except Exception:
        return False


# Cpf Checker
def check_cpf(doc: int):

    try:

        doc = cpf.mask(str(doc))
        checker = cpf.validate(doc)

        if checker is True:
            return checker

        return False

    except Exception:
        return False


# Email Checker
def check_email(contact: schemas.ContactsBase):

    try:

        checker = []
        contact_emails = [contact.email_01, contact.email_02, contact.email_03]

        for i in range(0, len(contact_emails)):

            if "@" in contact_emails[i]:

                email_checker = validate_email(contact_emails[i], dns_resolver=resolver).email

                if email_checker:
                    checker.append(True)

                else:
                    checker.append(False)

            else:
                checker.append(True)

        return checker

    except EmailNotValidError:
        return False

    except Exception:
        return False


# Read Contacts
def get_all_contacts(db: Session):
    all_contacts = db.query(models.Contacts).all()
    return all_contacts


# Read Contact by it's ID
def get_contact_by_id(contact_id: int, db: Session):

    db_contact = db.query(models.Contacts).filter(
        models.Contacts.id == contact_id).first()

    return db_contact


# Read Contact by it's phone
def get_contact_by_phone(contact_phone: str, db: Session):

    db_contact = db.query(models.Contacts).filter(
        models.Contacts.phone_01 == contact_phone).first()

    if db_contact:
        return db_contact

    else:
        db_contact = db.query(models.Contacts).filter(
            models.Contacts.phone_02 == contact_phone).first()

        if db_contact:
            return db_contact

        else:
            db_contact = db.query(models.Contacts).filter(
                models.Contacts.phone_03 == contact_phone).first()

            if db_contact:
                return db_contact


# Create Contact
def create_contact(contact: schemas.ContactsCreate, db: Session):

    try:

        # Validate size of phone number
        phone_checker = check_phone(contact)

        if(False not in phone_checker):

            # CPF and Email Checkers
            cpf_checker = check_cpf(contact.cpf)
            email_checker = check_email(contact)
            # print(cpf_checker, email_checker)

            if(cpf_checker is True and False not in email_checker):

                # Add new contact in database
                new_contact = models.Contacts(name=contact.name,
                                              last_name=contact.last_name,
                                              phone_01=contact.phone_01,
                                              phone_02=contact.phone_02,
                                              phone_03=contact.phone_03,
                                              cpf=contact.cpf,
                                              email_01=contact.email_01,
                                              email_02=contact.email_02,
                                              email_03=contact.email_03)
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
            detail="Phone must have at least 8 digits."
        )

    except Exception as e:
        print(e)
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
