# Here I created the connection to the database.

from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.orm import sessionmaker


engine = create_engine("mysql+pymysql://root@localhost:3306/db_new")

if database_exists(engine.url):
    pass
else:
    create_database(engine.url)


Session = sessionmaker()

local_session = Session(bind=engine)
