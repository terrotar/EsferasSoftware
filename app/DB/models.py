
import sqlalchemy as sql

from DB.database import Base


# Class Contact
class Contacts(Base):
    # Table's name
    __tablename__ = 'Contatos'

    # Attributes
    id = sql.Column(sql.Integer(), primary_key=True, autoincrement=True)
    name = sql.Column(sql.String(), nullable=False)
    last_name = sql.Column(sql.String(), nullable=False)
    cpf = sql.Column(sql.String(), default="")
    email_01 = sql.Column(sql.String(), default="")
    email_02 = sql.Column(sql.String(), default="")
    email_03 = sql.Column(sql.String(), default="")
    phone_01 = sql.Column(sql.String(), nullable=False)
    phone_02 = sql.Column(sql.String(), default="")
    phone_03 = sql.Column(sql.String(), default="")
