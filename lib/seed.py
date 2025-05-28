from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.__init__ import Base
from models.farmer import Farmer
from models.lender import Lender
from models.rating import Rating
from models.record import Record
from faker import Faker
from random import choice

if __name__ == '__main__':
    engine = create_engine('sqlite:///lib/db/farmers.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Farmer).delete()
    session.query(Record).delete()
    session.query(Lender).delete()
    session.query(Rating).delete()
    session.commit()

    frank = Farmer(name="Frank Kamau", location="Kiambu")
    andrew = Farmer(name="Andrew Kanja", location="Nyeri")
    alice = Farmer(name="Alice Kirui", location="Thika")
    peter = Farmer(name="Peter Musau", location="Limuru")
    david = Farmer(name="David Wahome", location="Kiambu")
    james = Farmer(name="James Kariuki", location="Limuru")
    diane = Farmer(name="Diane Muthoni", location="Kiambu")
    susan = Farmer(name="Susan Mutua", location="Nyeri")

    farmers = [frank, andrew, alice, peter, david, james, diane, susan]
    session.add_all(farmers)
    session.commit()

    records = [
        Record.create(farmer_id=frank.id, current_sales=50000, current_costs=23000,
                      current_liabilities=45000, asset_value=150000, session=session),
        Record.create(farmer_id=andrew.id, current_sales=30000, current_costs=17500,
                      current_liabilities=40000, asset_value=85000, session=session),
        Record.create(farmer_id=alice.id, current_sales=130000, current_costs=79000,
                      current_liabilities=200000, asset_value=350000, session=session),
        Record.create(farmer_id=peter.id, current_sales=140000, current_costs=95000,
                      current_liabilities=230000, asset_value=300000, session=session),
        Record.create(farmer_id=david.id, current_sales=55000, current_costs=45000,
                      current_liabilities=56000, asset_value=80000, session=session),
        Record.create(farmer_id=james.id, current_sales=100000, current_costs=75500,
                      current_liabilities=175000, asset_value=250000, session=session),
        Record.create(farmer_id=diane.id, current_sales=70000, current_costs=49000,
                      current_liabilities=70000, asset_value=85000, session=session),
        Record.create(farmer_id=susan.id, current_sales=57000, current_costs=35000,
                      current_liabilities=50000, asset_value=95000, session=session)
    ]

    session.add_all(records)
    session.commit()

    equity = Lender(name='Equity Bank')
    absa = Lender(name='ABSA Bank')
    kcb = Lender(name='KCB Bank')
    family = Lender(name='Family Bank')

    lenders = [equity, absa, kcb, family]

    session.add_all(lenders)
    session.commit()

    fake = Faker()
    farmers = session.query(Farmer).all()
    lenders = session.query(Lender).all()
    for i in range(10):
        farmer = choice(farmers)
        lender = choice(lenders)
        value = fake.random_int(min=1, max=10)

        rating = Rating.create(
            lender_id=lender.id,
            farmer_id=farmer.id,
            rating=value,
            session=session
        )
        session.add(rating)
    session.commit()
