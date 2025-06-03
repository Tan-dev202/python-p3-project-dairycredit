from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
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

    farmers = Farmer.get_all(session)
    lenders = Lender.get_all(session)
    ratings = Rating.get_all(session)
    records = Record.get_all(session)

    print("-----Testing DairyCredit App with UPDATE functionality-----")

    print(f"Total Farmers: {len(farmers)}")
    print(f"Total Lenders: {len(lenders)}")
    print(f"Total Ratings: {len(ratings)}")
    print(f"Total Records: {len(records)}")

    fake = Faker()

    farmer = Farmer.create(
        name=fake.name(),
        location=fake.city(),
        session=session
    )

    record = Record.create(
        farmer_id=farmer.id,
        current_sales=fake.random_int(min=10000, max=200000),
        current_costs=fake.random_int(min=5000, max=150000),
        current_liabilities=fake.random_int(min=1000, max=100000),
        asset_value=fake.random_int(min=50000, max=500000),
        session=session
    )

    print(f"Added a new farmer: {farmer.name} with credit score: {record.credit_score:.2f}")

    print("\n--- Updating Farmers ---")

    old_name = farmer.name
    farmer.update(session, name="Updated " + old_name, location="Updated Location")
    print(f"Updated farmer name from '{old_name}' to '{farmer.name}'")

    old_sales = record.current_sales
    old_score = record.credit_score
    record.update(session, current_sales=old_sales + 10000, asset_value=record.asset_value + 50000)
    print(f"Updated record sales from {old_sales} to {record.current_sales}")
    print(f"Credit score changed from {old_score:.2f} to {record.credit_score:.2f}")

    records = Record.get_all(session)
    scores = [record.credit_score for record in records if record.credit_score]
    if scores:
        print(f"\nAverage credit score: {sum(scores)/len(scores):.2f}")
        print(f"Highest credit score: {max(scores):.2f}")
        print(f"Lowest credit score: {min(scores):.2f}")

    import ipdb
    ipdb.set_trace()
