from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from datetime import date
from models.__init__ import Base

class Lender(Base):
    __tablename__ = 'lenders'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    ratings = relationship('Rating', back_populates='lender')

    def __repr__(self):
        return f"<Lender(id={self.id}, name='{self.name}')>"
