from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from models import Customer, OrderDetail
from utils.nice_print import print_record, print_records

engine = create_engine('sqlite:///db/lesson.db')  
Session = sessionmaker(bind=engine)
session = Session()

stmt = select(Customer).where(Customer.CustomerID == 5)

result = session.execute(stmt)
customer = result.scalar_one_or_none()
if customer:
    print_record(customer)
    print_records(customer.orders)
    print_records(customer.orders[0].orderdetails)
    od = OrderDetail(ProductID=1, Quantity=4,order=customer.orders[0])
    session.add(od)
    # customer.orders[0].orderdetails.append(od)
    session.commit()
    session.refresh(customer)
    print_records(customer.orders[0].orderdetails)                                     
else:
    print("Customer not found.")
