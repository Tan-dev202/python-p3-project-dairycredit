from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from datetime import date
from models.__init__ import Base


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

    @property
    def farmer_name(self):
        return len(self.name) >= 3 if self.name else False

    @property
    def farmer_location(self):
        return len(self.location) >= 3 if self.location else False

    @classmethod
    def create(cls, name, location, session):
        if not name or len(name) < 3:
            raise ValueError("Name must be at least 3 characters long")
        if not location or len(location) < 3:
            raise ValueError("Location must be at least 3 characters long")

        farmer = cls(name=name, location=location)
        session.add(farmer)
        session.commit()
        return farmer

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, farmer_id, session):
        return session.query(cls).filter(cls.id == farmer_id).first()

    @classmethod
    def find_by_name(cls, session):
        return session.query(cls).filter(cls.name).all()

    @classmethod
    def find_by_location(cls, session):
        return session.query(cls).filter(cls.location).all()

    def delete(self, session):
        session.delete(self)
        session.commit()

    def latest_record(self, session):
        from models.record import Record
        return session.query(Record).filter(Record.farmer_id == self.id).order_by(Record.record_date.desc()).first()
