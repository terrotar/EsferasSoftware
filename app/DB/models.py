
import sqlalchemy as sql

from DB.database import Base

from validate_docbr import CPF

from email_validator import validate_email, EmailNotValidError, caching_resolver


# Instance of CPF checker
cpf = CPF()


# Set a timeout for email checker
resolver = caching_resolver(timeout=10)


# Class Contact
class Contacts(Base):
    # Table's name
    __tablename__ = 'Contatos'

    # Attributes
    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    name = sql.Column(sql.String(30), nullable=False)
    last_name = sql.Column(sql.String(30), nullable=False)
    cpf = sql.Column(sql.String(14), unique=True)
    email = sql.Column(sql.String(), unique=True)
    phone = sql.Column(sql.Integer(), unique=True, nullable=False)

    # METHODS
    # Cpf Checker
    def check_cpf(self):

        self.cpf = cpf.mask(self.cpf)
        checker = cpf.validate(self.cpf)

        return checker

    # Email Checker
    def check_email(self):

        try:
            checker = validate_email(self.email, dns_resolver=resolver).email
            return checker

        except EmailNotValidError:
            return False

        except Exception:
            return False
