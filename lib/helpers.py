from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.__init__ import Base

engine = create_engine('sqlite:///lib/db/farmers.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def show_farmers(farmers):
    session = Session()

    print(f"\n{'ID':<5} {'Name':<20} {'Location':<15} {'Credit Score':<10}")
    print("-" * 50)

    for farmer in farmers:
        latest = farmer.latest_record(session)
        score = f"{latest.credit_score:.2f}" if latest else "Not available"
        print(f"{farmer.id:<5} {farmer.name:<20} {farmer.location:<15} {score:<10}")


def show_records(records):

    print(
        f"\n{'ID':<5} {'Farmer':<15} {'Sales':<10} {'Credit Score':<10} {'Date':<15}")
    print("-" * 50)

    for record in records:
        farmer_name = record.farmer.name if record.farmer else "Not available"
        print(f"{record.id:<5} {farmer_name:<15} {record.current_sales:<10} "
              f"{record.credit_score:<10} {record.record_date}")


def show_lenders(lenders):

    print(f"\n{'ID':<5} {'Name':<30}")
    print("-" * 50)

    for lender in lenders:
        print(f"{lender.id:<5} {lender.name:<30}")


def show_ratings(ratings):

    print(f"\n{'ID':<5} {'Lender':<20} {'Farmer':<20} {'Rating':<5}")
    print("-" * 50)

    for rating in ratings:
        lender_name = rating.lender.name if rating.lender else "Not available"
        farmer_name = rating.farmer.name if rating.farmer else "Not available"
        print(f"{rating.id:<5} {lender_name:<20} {farmer_name:<20} {rating.rating:<5}")


def confirm_delete(item_type, item_name):
    response = input(
        f"Delete {item_type} '{item_name}'? (yes/no): ").lower()
    return response == 'yes'
