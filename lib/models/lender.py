from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.__init__ import Base

class Lender(Base):
    __tablename__ = 'lenders'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    ratings = relationship('Rating', back_populates='lender')

    def __repr__(self):
        return f"<Lender(id={self.id}, name='{self.name}')>"
    
    @property
    def lender_name(self):
        return len(self.name) >= 3 if self.name else False
    
    @classmethod
    def create(cls, name, session):
        if not name or len(name) < 3:
            raise ValueError("Lender name must be at least 3 characters long")
        
        lender = cls(name=name)
        session.add(lender)
        session.commit()
        return lender
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, lender_id, session):
        return session.query(cls).filter(cls.id == lender_id).first()
    
    @classmethod
    def find_by_name(cls, session):
        return session.query(cls).filter(cls.name).all()
    
    def delete(self, session):
        session.delete(self)
        session.commit()
