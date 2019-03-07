from sqlalchemy import Column, Integer, String

from models.base import Base

class Upload(Base):
    """Represents the upload table"""
    __table_args__ = {
        'schema': 'calls'
    }
    __tablename__ = 'upload'
    id = Column(Integer, primary_key=True)
    filepath = Column(String, unique=True)