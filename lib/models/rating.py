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

    @classmethod
    def create(cls, lender_id, farmer_id, rating, session):
        if not (1 <= rating <= 10):
            raise ValueError("Rating must be between 1 and 10")

        entries = cls(lender_id=lender_id, farmer_id=farmer_id, rating=rating)
        session.add(entries)
        session.commit()
        return entries
