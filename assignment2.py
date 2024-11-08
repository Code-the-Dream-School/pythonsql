from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from models import Customer, OrderDetail, Order, Product
from utils.nice_print import print_record, print_records

engine = create_engine('sqlite:///db/lesson.db', echo=True, echo_pool="debug")  
Session = sessionmaker(bind=engine)
session = Session()

stmt = select(Customer).where(Customer.CustomerID == 5)

result = session.execute(stmt)
customer = result.scalar_one_or_none()
if customer:
    print_record(customer)
    print_records(customer.orders)
    print_records(customer.orders[0].orderdetails)
    od = OrderDetail(ProductID=1, Quantity=39,order=customer.orders[0])
    session.add(od)
    print("after add")
    print_records(customer.orders[0].orderdetails)
    session.refresh(customer.orders[0])
    print("after 0 refresh")
    print_record(customer.orders[0])
    # customer.orders[0].orderdetails.append(od)
    session.commit()
    print("before refresh 1")
    print_record(od)
    session.refresh(od)
    print("after refresh 1")
    print_record(od)
    print_records(customer.orders[0].orderdetails)
    session.refresh(customer)
    print_records(customer.orders[0].orderdetails) 
else:
    print("Customer not found.")

session.close()
session=Session()

stmt = select(Order).limit(1)
order = session.scalars(stmt).first()
print_record(order)
print_records(order.products)
session.close()