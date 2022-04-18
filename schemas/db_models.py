# Here I created the database models of the two tables needed for this api.

from sqlalchemy import Column, String, Integer, BigInteger, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base
from config.db_config import engine

Base = declarative_base()


class PandorasUsersDB(Base):
    __tablename__="PandorasUsersDB"
    user_id = Column(Integer, nullable=False, unique=True, autoincrement=True, primary_key=True)
    first_name = Column(String(length=60), unique=False, nullable=False)
    last_name = Column(String(length=70), unique=False, nullable=False)
    username = Column(String(length=60), nullable=False, unique=True)
    hashed_password = Column(String(length=200), nullable=False, unique=False)
    email = Column(String(length=150), nullable=False, unique=True)
    cellphone = Column(BigInteger, nullable=True, unique=False)
    disabled = Column(Boolean, nullable=False, unique=False, default=False)


### You should use FOREIGNKEY for the foreign key.
class PandorasMisteriesDB(Base):
    __tablename__="PandorasMisteriesDB"
    mistery_id = Column(Integer, nullable=False, unique=True, primary_key=True)
    mistery_title = Column(String(length=100), nullable=False, unique=False)
    password = Column(String(length=200), nullable=False, unique=False)
    mistery_token = Column(String(length=250), nullable=True, unique=False, default=None)
    username = Column(String(length=70), nullable=True, unique=True)
    email = Column(String(length=100), nullable=True, unique=False, default=None)
    description = Column(String(length=300), nullable=True, unique=False, default=None)
    url = Column(String(length=200), nullable=True, unique=False, default=None)
    other = Column(String(length=200), nullable=True, unique=False, default=None)
    foreign_key = Column(Integer, nullable=False, unique=False)
    disabled = Column(Boolean, nullable=False, unique=False, default=False)


Base.metadata.create_all(engine)
