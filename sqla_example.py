from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from models import Product, Order, Customer, Lineitem
from utils.nice_print import print_record, print_records, print_rows # Provided for your convenience

engine = create_engine('sqlite:///db/lesson.db', echo=True, echo_pool="debug")  
Session = sessionmaker(bind=engine)

with Session() as session:
    product = session.query(Product).first()
    print_record(product)
    stmt = select(Product).limit(3) # This just builds the statement.
    products = session.scalars(stmt).all() # Here the statement is executed and the results obtained
    print_records(products)
    stmt = select(Product.product_name, Product.price).select_from(Product).limit(5)
    result = session.execute(stmt)
    product_attributes = result.fetchall()
    print_rows(product_attributes)
    stmt = select(Customer.customer_name, Order.order_id).select_from(Customer) \
    .join(Order).limit(5)
    result = session.execute(stmt)
    customer_orders = result.fetchall()
    print_rows(customer_orders)
    session.close()

added_line_item = 0
first_order = 0
with Session() as session:
    stmt = select(Order).limit(1)
    order = session.scalars(stmt).first() # there ought to be some conditional logic here
    first_order = order.order_id # the table might not exist, or it might be empty
    print_record(order)
    print_record(order.customer)
    print_record(order.employee)
    print_records(order.line_items)
    print_records(order.products)
    session.close()

with Session() as session:
    order = session.get(Order,{"order_id": first_order})
    li = Lineitem(product_id=1, quantity=26, order=order)
    session.add(li)
    try:
        session.commit()
    except Exception as e:
        print(f"We had an exception on the commit: {e}")
        session.rollback()
    else:
        print_records(order.line_items)
        added_line_item=li.line_item_id
    session.close()

with Session() as session:
    li_for_update = session.get(Lineitem, added_line_item, with_for_update=True)
    if li_for_update:
        li_for_update.quantity += 40
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"We had an exception on the commit of an update: {e}")
        else:
            print_records(li_for_update.order.line_items)
    session.close()

with Session() as session:
    li_for_delete = session.get(Lineitem, added_line_item)
    if li_for_delete:
        session.delete(li_for_delete)
        try: 
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"We had an exception committing the delete. {e}")
        else:
            order_one = session.get(Order, {"order_id": first_order})
            if order_one:
                print_records(order_one.line_items)
    session.close()
    
