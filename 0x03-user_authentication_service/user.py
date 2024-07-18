#!/usr/bin/env python3
"""sqlalchemy model"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class User(Base):
    """Create user class"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)
