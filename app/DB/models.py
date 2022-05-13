
import sqlalchemy as sql

from DB.database import Base


# Class Contact
class Contacts(Base):
    # Table's name
    __tablename__ = 'Contatos'

    # Attributes
    id = sql.Column(sql.Integer(), primary_key=True, autoincrement=True)
    name = sql.Column(sql.String(30), nullable=False)
    last_name = sql.Column(sql.String(30), nullable=False)
    cpf = sql.Column(sql.String(14), unique=True, default="")
    email = sql.Column(sql.String(), unique=True, default="")
    phone = sql.Column(sql.Integer(), unique=True, nullable=False)
