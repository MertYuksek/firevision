from enum import unique
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base


class Contents(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, nullable=False)
    lat = Column(Integer, nullable=False)
    lon = Column(Integer, nullable=False)
    is_fire = Column(Boolean, server_default='False', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text("now()"))


class Objects(Base):
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)


class Contents_Objects(Base):
    __tablename__ = "contents_objects"

    content_id = Column(Integer, ForeignKey(
            "contents.id", ondelete="CASCADE"), primary_key=True)
    object_id = Column(Integer, ForeignKey(
            "objects.id", ondelete="CASCADE"), primary_key=True)
    count = Column(Integer, nullable=False)
