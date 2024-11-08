from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
from models import Product, Supplier, Order, OrderDetail, Shipper, Customer, Employee, Category
from utils.nice_print import print_record, print_records, print_rows # Provided for your convenience

engine = create_engine('sqlite:///db/lesson.db', echo=True, echo_pool="debug")  
Session = sessionmaker(bind=engine)

__all__ = ['select', 'func', 'Product', 'Supplier', 'Order', 'OrderDetail', 'Shipper',
            'Customer', 'Employee', 'Category', 'print_record',
            'print_records', 'print_rows', 'Session']