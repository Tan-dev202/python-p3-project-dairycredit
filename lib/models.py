from sqlalchemy import MetaData, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import date


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
    
    records = relationship('Record', back_populates='farmer')
    ratings = relationship('Rating', back_populates='farmer')

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
    
    farmer = relationship('Farmer', back_populates='records')

    def __repr__(self):
        return f"<Record(id={self.id}, farmer_id={self.farmer_id}, credit_score={self.credit_score:.2f})>"
    
    def calculate_credit_score(self):
        if self.current_sales == 0 or self.asset_value == 0:
            return 0
        
        cost_to_sales_ratio = (self.current_costs / self.current_sales) * 100
        liabilities_to_assets_ratio = (self.current_liabilities / self.asset_value) * 100
        average_ratio = (cost_to_sales_ratio + liabilities_to_assets_ratio) / 2
        
        credit_score = 100 - average_ratio
        return round(max(0, credit_score), 2)

    @classmethod
    def create(cls, farmer_id, current_sales, current_costs, current_liabilities, asset_value, session):
        farmer = session.query(Farmer).filter(Farmer.id == farmer_id).first()
        if not farmer:
            raise ValueError("Farmer not found")
        
        record = cls(
            farmer_id=farmer_id,
            current_sales=current_sales,
            current_costs=current_costs,
            current_liabilities=current_liabilities,
            asset_value=asset_value
        )
        record.credit_score = record.calculate_credit_score()
        
        session.add(record)
        session.commit()
        return record

class Lender(Base):
    __tablename__ = 'lenders'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    
    ratings = relationship('Rating', back_populates='lender')

    def __repr__(self):
        return f"<Lender(id={self.id}, name='{self.name}')>"


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
        
        review = cls(lender_id=lender_id, farmer_id=farmer_id, rating=rating)
        session.add(review)
        session.commit()
        return review
