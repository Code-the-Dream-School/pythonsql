from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from models import Customer  
from utils.nice_print import print_records, print_rows

engine = create_engine('sqlite:///db/lesson.db')  
Session = sessionmaker(bind=engine)
session = Session()

print("Retrieve all customers, first using query:\n")
all_customers = session.query(Customer).all()
print_records(all_customers)

print("\nRetrieve all customers, using select\n")
stmt = select(Customer)
all_customers = session.scalars(stmt).all()
print_records(all_customers)


print("\nRetrieve just the customer name and country.\n")
stmt = select(Customer.CustomerName, Customer.Country)
result = session.execute(stmt)
all_customers = result.fetchall()
print_rows(all_customers)

session.close()
