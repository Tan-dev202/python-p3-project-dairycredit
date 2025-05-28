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
    
