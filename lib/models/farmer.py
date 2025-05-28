from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from models.__init__ import Base

# convention = {
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
# }
# metadata = MetaData(naming_convention=convention)

# Base = declarative_base(metadata=metadata)

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

