from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .config import mysql_settings

HOST = mysql_settings.HOST
USER = mysql_settings.USER
PASS = mysql_settings.PASS
PORT = mysql_settings.PORT
DATABASE = mysql_settings.DATABASE

mysql_url = f"mysql+mysqlconnector://{USER}:{PASS}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(
    mysql_url, pool_size=10, max_overflow=5, pool_timeout=30, pool_recycle=1800
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class DatabaseSession:
    def __init__(self):
        self.db = None

    def __enter__(self) -> Session:
        self.db = SessionLocal()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                self.db.commit()
            else:
                self.db.rollback()
        finally:
            self.db.close()
