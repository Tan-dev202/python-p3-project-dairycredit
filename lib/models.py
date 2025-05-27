from sqlalchemy import MetaData, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, date

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Farmer(Base):
    __tablename__ = 'farmers'
    
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    location = Column(String())
    registration_date = Column(Date(), default=date.today)
    
    def __repr__(self):
        return f'<Farmer(id={self.id}, name={self.name}, location={self.location})>'

class Record(Base):
    __tablename__ = 'records'
    
    id = Column(Integer(), primary_key=True)
    farmer_id = Column(Integer(), ForeignKey('farmers.id'))
    current_sales = Column(Float())
    current_costs = Column(Float())
    current_liabilities = Column(Float())
    asset_value = Column(Float())
    credit_score = Column(Float())
    record_date = Column(Date(), default=date.today)
    
    def __repr__(self):
        return f"<Record(id={self.id}, farmer_id={self.farmer_id}, credit_score={self.credit_score})>"

class Lender(Base):
    __tablename__ = 'lenders'
    
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    
    def __repr__(self):
        return f"<Lender(id={self.id}, name='{self.name}')>"

class Rating(Base):
    __tablename__ = 'ratings'
    
    id = Column(Integer(), primary_key=True)
    lender_id = Column(Integer(), ForeignKey('lenders.id'))
    farmer_id = Column(Integer(), ForeignKey('farmers.id'))
    rating = Column(Integer())
    rating_date = Column(Date(), default=date.today)
    
    def __repr__(self):
        return f"<Rating(id={self.id}, lender_id={self.lender_id}, farmer_id={self.farmer_id}, rating={self.rating})>"
    