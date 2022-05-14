
from typing import Optional

import pydantic as pydantic


class ContactsBase(pydantic.BaseModel):
    name: str
    last_name: str
    cpf: Optional[str] = None
    email_01: Optional[str] = None
    email_02: Optional[str] = None
    email_03: Optional[str] = None
    phone_01: str
    phone_02: Optional[str] = None
    phone_03: Optional[str] = None


class ContactsCreate(ContactsBase):
    pass

    class Config:
        orm_mode = True


class Contacts(ContactsBase):
    id: int

    class Config:
        orm_mode = True
