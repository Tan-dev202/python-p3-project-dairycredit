from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from models.__init__ import Base


class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer(), primary_key=True)
    lender_id = Column(Integer(), ForeignKey('lenders.id'))
    farmer_id = Column(Integer(), ForeignKey('farmers.id'))
    rating = Column(Integer())
    rating_date = Column(Date(), default=date.today)

    lender = relationship('Lender', back_populates='ratings')
    farmer = relationship('Farmer', back_populates='ratings')

    def __repr__(self):
        return f"<Rating(id={self.id}, lender_id={self.lender_id}, farmer_id={self.farmer_id}, rating={self.rating})>"

    @property
    def farmer_rating(self):
        return 1 <= self.rating <= 10 if self.rating else False

    @classmethod
    def create(cls, lender_id, farmer_id, rating, session):
        if not (1 <= rating <= 10):
            raise ValueError("Rating must be between 1 and 10")

        from models.lender import Lender
        lender = session.query(Lender).filter(Lender.id == lender_id).first()

        from models.farmer import Farmer
        farmer = session.query(Farmer).filter(Farmer.id == farmer_id).first()

        if not lender:
            raise ValueError("Lender not found")
        if not farmer:
            raise ValueError("Farmer not found")

        entries = cls(lender_id=lender_id, farmer_id=farmer_id, rating=rating)
        session.add(entries)
        session.commit()
        return entries

    def update(self, session, rating=None):
        if rating is not None:
            if not (1 <= rating <= 10):
                raise ValueError("Rating must be between 1 and 10")
            self.rating = rating
        
        session.commit()
        return self
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, rating_id, session):
        return session.query(cls).filter(cls.id == rating_id).first()
    
    @classmethod
    def find_by_farmer_id(cls, farmer_id, session):
        return session.query(cls).filter(cls.farmer_id == farmer_id).all()
    
    @classmethod
    def find_by_lender_id(cls, lender_id, session):
        return session.query(cls).filter(cls.lender_id == lender_id).all()
    
    def delete(self, session):
        session.delete(self)
        session.commit()
