from models.farmer import Farmer
from models.lender import Lender
from models.rating import Rating
from models.record import Record

from helpers import (show_farmers, show_records,
                     show_lenders, show_ratings, confirm_update, confirm_delete, Session)


class App:
    def run(self):
        while True:
            print("\n" + "-"*40)
            print("⠋ DairyCredit App ⠋")
            print("-"*40)
            print("1. Farmers")
            print("2. Records")
            print("3. Lenders")
            print("4. Ratings")
            print("5. Exit")

            choice = int(input("Choose option (1-5): "))

            if choice == 1:
                self.farmer_menu()
            elif choice == 2:
                self.record_menu()
            elif choice == 3:
                self.lender_menu()
            elif choice == 4:
                self.rating_menu()
            else:
                print("Thank you for using DairyCredit App!")
                break

    def farmer_menu(self):
        session = Session()
        try:
            while True:
                print("\n--- Farmers ---")
                print("1. Add Farmer")
                print("2. View All")
                print("3. Find by ID")
                print("4. Search by Name")
                print("5. Update Farmer")
                print("6. Delete")
                print("7. Go back")

                choice = int(input("Choose (1-7): "))

                if choice == 1:
                    self.add_farmer()
                elif choice == 2:
                    show_farmers(Farmer.get_all(session))
                elif choice == 3:
                    self.find_farmer()
                elif choice == 4:
                    self.search_farmers()
                elif choice == 5:
                    self.update_farmer()
                elif choice == 6:
                    self.delete_farmer()
                else:
                    break
        finally:
            session.close()

    def record_menu(self):
        session = Session()
        try:
            while True:
                print("\n--- Records ---")
                print("1. Add Record")
                print("2. View All")
                print("3. Find by ID")
                print("4. View by Farmer")
                print("5. Update Record")
                print("6. Delete")
                print("7. Go back")

                choice = int(input("Choose (1-7): "))

                if choice == 1:
                    self.add_record()
                elif choice == 2:
                    show_records(Record.get_all(session))
                elif choice == 3:
                    self.find_record()
                elif choice == 4:
                    self.records_by_farmer()
                elif choice == 5:
                    self.update_record()
                elif choice == 6:
                    self.delete_record()
                else:
                    break
        finally:
            session.close()

    def lender_menu(self):
        session = Session()
        try:
            while True:
                print("\n--- Lenders ---")
                print("1. Add Lender")
                print("2. View All")
                print("3. Find by ID")
                print("4. Update Lender")
                print("5. Delete")
                print("6. Go back")

                choice = int(input("Choose (1-6): "))

                if choice == 1:
                    self.add_lender()
                elif choice == 2:
                    show_lenders(Lender.get_all(session))
                elif choice == 3:
                    self.find_lender()
                elif choice == 4:
                    self.update_lender()
                elif choice == 5:
                    self.delete_lender()
                else:
                    break
        finally:
            session.close()

    def rating_menu(self):
        session = Session()
        try:
            while True:
                print("\n--- Ratings ---")
                print("1. Add Rating")
                print("2. View All")
                print("3. Find by ID")
                print("4. Update Rating")
                print("5. Delete")
                print("6. Go back")

                choice = int(input("Choose (1-6): "))

                if choice == 1:
                    self.add_rating()
                elif choice == 2:
                    show_ratings(Rating.get_all(session))
                elif choice == 3:
                    self.find_rating()
                elif choice == 4:
                    self.update_rating()
                elif choice == 5:
                    self.delete_rating()
                else:
                    break
        finally:
            session.close()

    def add_farmer(self):
        session = Session()
        try:
            name = input("Farmer name: ")
            location = input("Location: ")
            farmer = Farmer.create(
                name=name, location=location, session=session)
            print(f"✔ Added farmer '{farmer.name}' (ID: {farmer.id})")
        except Exception as exc:
            print(f"⠋ Error: {exc}")
        finally:
            session.close()

    def find_farmer(self):
        session = Session()
        farmer_id = int(input("Farmer ID: "))
        farmer = Farmer.find_by_id(farmer_id, session)
        if farmer:
            print(f"\nID: {farmer.id}")
            print(f"Name: {farmer.name}")
            print(f"Location: {farmer.location}")
            print(f"Records: {len(farmer.records)}")
        else:
            print("⠋ Farmer not found")

    def search_farmers(self):
        session = Session()
        name = input("Search name: ")
        farmers = Farmer.find_by_name(name, session)
        if farmers:
            show_farmers(farmers)
        else:
            print("⠋ No farmers found")

    def update_farmer(self):
        session = Session()
        try:
            farmer_id = int(input("Farmer ID to update: "))
            farmer = Farmer.find_by_id(farmer_id, session)

            if not farmer:
                print("⠋ Farmer not found")
                return

            print(f"Current farmer: {farmer.name} from {farmer.location}")

            if confirm_update("farmer", farmer.name):
                name = input(
                    f"New name (current: {farmer.name}, press Enter to skip): ")
                location = input(
                    f"New location (current: {farmer.location}, press Enter to skip): ")

                changes = {}
                if name:
                    changes['name'] = name
                if location:
                    changes['location'] = location

                if changes:
                    farmer.update(session, **changes)
                    print(f"✔ Farmer updated successfully")
                else:
                    print("⠋ No changes made")

        except Exception as exc:
            print(f"⠋ Error: {exc}")
        finally:
            session.close()

    def delete_farmer(self):
        session = Session()
        farmer_id = int(input("Farmer ID to delete: "))
        farmer = Farmer.find_by_id(farmer_id, session)
        if farmer and confirm_delete("farmer", farmer.name):
            farmer.delete(session)
            print("✔ Farmer deleted")
        elif not farmer:
            print("⠋ Farmer not found")

    def add_record(self):
        session = Session()
        try:
            farmers = Farmer.get_all(session)

            show_farmers(farmers)
            farmer_id = int(input("Farmer ID: "))

            sales = float(input("Sales: "))
            costs = float(input("Costs: "))
            liabilities = float(input("Liabilities: "))
            assets = float(input("Assets: "))

            record = Record.create(
                farmer_id=farmer_id,
                current_sales=sales,
                current_costs=costs,
                current_liabilities=liabilities,
                asset_value=assets,
                session=session
            )

            print(
                f"✔ Record added (ID: {record.id}, Score: {record.credit_score:.2f})")
        except Exception as exc:
            print(f"⠋ Error: {exc}")
        finally:
            session.close()

    def find_record(self):
        session = Session()
        record_id = int(input("Record ID: "))
        record = Record.find_by_id(record_id, session)
        if record:
            print(f"\nID: {record.id}")
            print(f"Farmer: {record.farmer.name}")
            print(f"Sales: {record.current_sales}")
            print(f"Costs: {record.current_costs}")
            print(f"Liabilities: {record.current_liabilities}")
            print(f"Assets: {record.asset_value}")
            print(f"Credit Score: {record.credit_score:.2f}")
            print(f"Date: {record.record_date}")
        else:
            print("⠋ Record not found")

    def records_by_farmer(self):
        session = Session()
        farmer_id = int(input("Farmer ID: "))
        farmer = Farmer.find_by_id(farmer_id, session)

        records = Record.find_by_farmer_id(farmer_id, session)
        print(f"\n--- Records for {farmer.name} ---")
        show_records(records)

    def update_record(self):
        session = Session()
        try:
            record_id = int(input("Record ID to update: "))
            record = Record.find_by_id(record_id, session)

            if not record:
                print("⠋ Record not found")
                return

            print(f"Current record for {record.farmer.name}:")
            print(
                f"Sales: {record.current_sales}, Costs: {record.current_costs}")
            print(
                f"Liabilities: {record.current_liabilities}, Assets: {record.asset_value}")
            print(f"Credit Score: {record.credit_score:.2f}")

            if confirm_update("record", f"ID {record.id}"):
                sales = input(
                    f"New sales (current: {record.current_sales}, press Enter to skip): ")
                costs = input(
                    f"New costs (current: {record.current_costs}, press Enter to skip): ")
                liabilities = input(
                    f"New liabilities (current: {record.current_liabilities}, press Enter to skip): ")
                assets = input(
                    f"New assets (current: {record.asset_value}, press Enter to skip): ")

                changes = {}
                if sales:
                    changes['current_sales'] = float(sales)
                if costs:
                    changes['current_costs'] = float(costs)
                if liabilities:
                    changes['current_liabilities'] = float(liabilities)
                if assets:
                    changes['asset_value'] = float(assets)

                if changes:
                    record.update(session, **changes)
                    print(
                        f"✔ Record updated successfully. New credit score: {record.credit_score:.2f}")
                else:
                    print("⠋ No changes made")

        except Exception as exc:
            print(f"⠋ Error: {exc}")
        finally:
            session.close()

    def delete_record(self):
        session = Session()
        record_id = int(input("Record ID to delete: "))
        record = Record.find_by_id(record_id, session)
        if record and confirm_delete("record", f"ID {record.id}"):
            record.delete(session)
            print("✔ Record deleted")
        elif not record:
            print("⠋ Record not found")

    def add_lender(self):
        session = Session()
        try:
            name = input("Lender name: ")
            lender = Lender.create(name=name, session=session)
            print(f"✔ Added lender '{lender.name}' (ID: {lender.id})")
        except Exception as exc:
            print(f"⠋ Error: {exc}")
        finally:
            session.close()

    def find_lender(self):
        session = Session()
        lender_id = int(input("Lender ID: "))
        lender = Lender.find_by_id(lender_id, session)
        if lender:
            print(f"\nID: {lender.id}")
            print(f"Name: {lender.name}")
            print(f"Ratings given: {len(lender.ratings)}")
        else:
            print("⠋ Lender not found")

    def update_lender(self):
        session = Session()
        try:
            lender_id = int(input("Lender ID to update: "))
            lender = Lender.find_by_id(lender_id, session)

            if not lender:
                print("⠋ Lender not found")
                return

            print(f"Current lender: {lender.name}")

            if confirm_update("lender", lender.name):
                name = input(
                    f"New name (current: {lender.name}, press Enter to skip): ")

                changes = {}
                if name:
                    changes['name'] = name

                if changes:
                    lender.update(session, **changes)
                    print(f"✔ Lender updated successfully")
                else:
                    print("⠋ No changes made")

        except Exception as exc:
            print(f"⠋ Error: {exc}")
        finally:
            session.close()

    def delete_lender(self):
        session = Session()
        lender_id = int(input("Lender ID to delete: "))
        lender = Lender.find_by_id(lender_id, session)
        if lender and confirm_delete("lender", lender.name):
            lender.delete(session)
            print("✔ Lender deleted")
        elif not lender:
            print("⠋ Lender not found")

    def add_rating(self):
        session = Session()
        try:
            lenders = Lender.get_all(session)
            farmers = Farmer.get_all(session)

            print("\nLenders:")
            show_lenders(lenders)
            lender_id = int(input("Lender ID: "))

            print("\nFarmers:")
            show_farmers(farmers)
            farmer_id = int(input("Farmer ID: "))

            rating_value = int(input("Rating (1-10): "))

            rating = Rating.create(
                lender_id=lender_id,
                farmer_id=farmer_id,
                rating=rating_value,
                session=session
            )

            print(f"✔ Rating added (ID: {rating.id})")
        except Exception as exc:
            print(f"⠋ Error: {exc}")
        finally:
            session.close()

    def find_rating(self):
        session = Session()
        rating_id = int(input("Rating ID: "))
        rating = Rating.find_by_id(rating_id, session)
        if rating:
            print(f"\nID: {rating.id}")
            print(f"Lender: {rating.lender.name}")
            print(f"Farmer: {rating.farmer.name}")
            print(f"Rating: {rating.rating}/10")
            print(f"Date: {rating.rating_date}")
        else:
            print("⠋ Rating not found")

    def update_rating(self):
        session = Session()
        try:
            rating_id = int(input("Rating ID to update: "))
            rating = Rating.find_by_id(rating_id, session)

            if not rating:
                print("⠋ Rating not found")
                return

            print(
                f"Current rating: {rating.rating}/10 by {rating.lender.name} for {rating.farmer.name}")

            if confirm_update("rating", f"ID {rating.id}"):
                new_rating = input(
                    f"New rating (current: {rating.rating}/10, press Enter to skip): ")

                changes = {}
                if new_rating:
                    changes['rating'] = int(new_rating)

                if changes:
                    rating.update(session, **changes)
                    print(f"✔ Rating updated successfully")
                else:
                    print("⠋ No changes made")

        except Exception as exc:
            print(f"⠋ Error: {exc}")
        finally:
            session.close()

    def delete_rating(self):
        session = Session()
        rating_id = int(input("Rating ID to delete: "))
        rating = Rating.find_by_id(rating_id, session)
        if rating and confirm_delete("rating", f"ID {rating.id}"):
            rating.delete(session)
            print("✔ Rating deleted")
        elif not rating:
            print("⠋ Rating not found")


def main():
    cli = App()
    cli.run()


if __name__ == "__main__":
    main()
