#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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

    print("-----Testing DairyCredit App-----")

    print(f"Total Farmers: {len(farmers)}")
    print(f"Total Lenders: {len(lenders)}")
    print(f"Total Ratings: {len(ratings)}")
    print(f"Total Records: {len(records)}")

    scores = [record.credit_score for record in records if record.credit_score]
    if scores:
        print(f"Average credit score: {sum(scores)/len(scores):.2f}")
        print(f"Highest credit score: {max(scores):.2f}")
        print(f"Lowest credit score: {min(scores):.2f}")

    import ipdb
    ipdb.set_trace()
