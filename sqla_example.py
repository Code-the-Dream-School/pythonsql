from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from models import Product, Supplier, Order, OrderDetail
from utils.nice_print import print_record, print_records, print_rows # Provided for your convenience

engine = create_engine('sqlite:///db/lesson.db', echo=True, echo_pool="debug")  
Session = sessionmaker(bind=engine)

with Session() as session:
    product = session.query(Product).first()
    print_record(product)
    stmt = select(Product).limit(3) # This just builds the statement.
    products = session.scalars(stmt).all() # Here the statement is executed and the results obtained
    print_records(products)
    stmt = select(Product.ProductName, Product.Price)
    result = session.execute(stmt)
    product_attributes = result.fetchall()
    print_rows(product_attributes)
    stmt = select(Product.ProductName, Supplier.SupplierName).join(Product.supplier).limit(5)
    result = session.execute(stmt)
    products_suppliers = result.fetchall()
    print_rows(products_suppliers)
    session.close()

added_order_detail = 0
first_order = 0
with Session() as session:
    stmt = select(Order).limit(1)
    order = session.scalars(stmt).first() # there ought to be some conditional logic here
    first_order = order.OrderID # the table might not exist, or it might be empty
    print_record(order)
    print_record(order.customer)
    print_record(order.shipper)
    print_record(order.employee)
    print_records(order.orderdetails)
    print_records(order.products)
    session.close()

with Session as session:
    order = session.get(Order,{"OrderID": first_order})
    od = OrderDetail(ProductID=1, Quantity=26, order=order)
    session.add(od)
    try:
        session.commit()
    except Exception as e:
        print("We had an exception on the commit: {e}")
        session.rollback()
    else:
        print_records(order.orderdetails)
        added_order_detail=od.OrderDetailID
    session.close()

with Session() as session:
    od_for_update = session.get(OrderDetail, {"OrderDetailID": added_order_detail}, with_for_update=True)
    if od_for_update:
        od_for_update.Quantity += 40
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            print("We had an exception on the commit of an update: {e}")
        else:
            print_records(od_for_update.order.orderdetails)
    session.close()

with Session() as session:
    od_for_delete = session.get(OrderDetail, {"OrderDetailID": added_order_detail})
    if od_for_delete:
        session.delete(od_for_delete)
        try: 
            session.commit()
        except Exception as e:
            session.rollback()
            print("We had an exception committing the delete.")
        else:
            order_one = session.get(Order, {"OrderID": first_order})
            if order_one:
                print_records(order_one.orderdetails)
    session.close()
    





