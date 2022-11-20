import uuid
from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Boolean, text,Float, Integer,DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    name = Column(String,  nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))


class Project(Base):
    __tablename__ = 'projects'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    username = Column(String, ForeignKey(
        'users.username', ondelete='CASCADE'), nullable=False)
    title = Column(String, nullable=False)
    zip_code = Column(Integer,nullable=False)
    cost = Column(Float(precision=2),nullable=False)
    done = Column(Boolean, default=False)
    deadline = Column(DateTime,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    user = relationship('User')
