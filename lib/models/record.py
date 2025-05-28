from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from models.__init__ import Base


class Record(Base):
    __tablename__ = 'records'

    id = Column(Integer(), primary_key=True)
    farmer_id = Column(Integer(), ForeignKey('farmers.id'))
    current_sales = Column(Integer())
    current_costs = Column(Integer())
    current_liabilities = Column(Integer())
    asset_value = Column(Integer())
    credit_score = Column(Float())
    record_date = Column(Date(), default=date.today)

    farmer = relationship('Farmer', back_populates='records')

    def __repr__(self):
        return f"<Record(id={self.id}, farmer_id={self.farmer_id}, credit_score={self.credit_score:.2f})>"
    
    @property
    def sales(self):
        return self.current_sales >= 0 if self.current_sales else False
    
    @property
    def costs(self):
        return self.current_costs >= 0 if self.current_costs else False
    
    @property
    def liabilities(self):
        return self.current_liabilities >= 0 if self.current_liabilities else False
    
    @property
    def assets(self):
        return self.asset_value > 0 if self.asset_value else False

    def calculate_credit_score(self):
        if self.current_sales == 0 or self.asset_value == 0:
            return 0

        cost_to_sales_ratio = (self.current_costs / self.current_sales) * 100
        liabilities_to_assets_ratio = (
            self.current_liabilities / self.asset_value) * 100
        average_ratio = (cost_to_sales_ratio + liabilities_to_assets_ratio) / 2

        credit_score = 100 - average_ratio
        return round(max(0, credit_score), 2)

    @classmethod
    def create(cls, farmer_id, current_sales, current_costs, current_liabilities, asset_value, session):
        
        if current_sales < 0:
            raise ValueError("Sales must be at least zero")
        if current_costs < 0:
            raise ValueError("Costs must be at least zero")
        if current_liabilities < 0:
            raise ValueError("Liabilities must be at least zero")
        if asset_value <= 0:
            raise ValueError("Asset value must be greater than zero")
        
        from models.farmer import Farmer
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
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, record_id, session):
        return session.query(cls).filter(cls.id == record_id).first()
    
    @classmethod
    def find_by_farmer_id(cls, farmer_id, session):
        return session.query(cls).filter(cls.farmer_id == farmer_id).all()
    
    def delete(self, session):
        session.delete(self)
        session.commit()
