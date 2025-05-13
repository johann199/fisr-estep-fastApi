import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqliteName = "movies.sqlite"
baseDir = os.path.dirname(os.path.realpath(__file__))
databaseUrl = f"sqlite:///{os.path.join(baseDir, sqliteName)}"
engine = create_engine(databaseUrl, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()