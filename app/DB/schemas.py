
from typing import Optional

import pydantic as pydantic


class ContactsBase(pydantic.BaseModel):
    name: str
    last_name: str
    cpf: Optional[str] = None
    email: Optional[str] = None
    phone: int


class ContactsCreate(ContactsBase):
    pass

    class Config:
        orm_mode = True


class Contacts(ContactsBase):
    id: int

    class Config:
        orm_mode = True
