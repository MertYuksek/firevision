from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:mert33yyy@localhost/firevision"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# Establish connection with db.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# We have to use Session to talk with db.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# We will inherit from this class to create each of the database models or classes (the ORM models)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

