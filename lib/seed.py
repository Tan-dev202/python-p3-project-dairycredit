from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from random import choice
from models.__init__ import Base
from models.farmer import Farmer
from models.lender import Lender
from models.rating import Rating
from models.record import Record


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

    farmers = [
        ("Frank Kamau", "Kiambu"),
        ("Andrew Kanja", "Nyeri"),
        ("Alice Kirui", "Thika"),
        ("Peter Musau", "Limuru"),
        ("David Wahome", "Kiambu"),
        ("James Kariuki", "Limuru"),
        ("Diane Muthoni", "Kiambu"),
        ("Susan Mutua", "Nyeri")
    ]

    farmers = [Farmer.create(name=name, location=location, session=session)
               for name, location in farmers]
    session.add_all(farmers)
    session.commit()

    farmer_map = {farmer.name: farmer for farmer in farmers}

    records = [
        ("Frank Kamau", 50000, 23000, 45000, 150000),
        ("Andrew Kanja", 30000, 17500, 40000, 85000),
        ("Alice Kirui", 130000, 79000, 200000, 350000),
        ("Peter Musau", 140000, 95000, 230000, 300000),
        ("David Wahome", 55000, 45000, 56000, 80000),
        ("James Kariuki", 100000, 75500, 175000, 250000),
        ("Diane Muthoni", 70000, 49000, 70000, 85000),
        ("Susan Mutua", 57000, 35000, 50000, 95000)
    ]

    records = [
        Record.create(
            farmer_id=farmer_map[name].id,
            current_sales=sales,
            current_costs=costs,
            current_liabilities=liabilities,
            asset_value=assets,
            session=session
        )
        for name, sales, costs, liabilities, assets in records
    ]

    session.add_all(records)
    session.commit()

    lender_names = ['Equity Bank', 'ABSA Bank', 'KCB Bank', 'Family Bank']
    lenders = [Lender.create(name=name, session=session)
               for name in lender_names]
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
