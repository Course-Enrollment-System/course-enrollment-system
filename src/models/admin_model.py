from sqlalchemy import Column, Integer, String

from src.config.database import Base

class AdminModel(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(224), nullable=False)
    email = Column(String(224), unique=True, nullable=False)
    password = Column(String(255), nullable=False)