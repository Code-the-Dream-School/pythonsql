from sqlalchemy import create_engine, select, func, any_, all_, exists, and_, or_, not_
from sqlalchemy.orm import sessionmaker
from models import Product, Order, Customer, Employee, Lineitem
from utils.nice_print import print_record, print_records, print_rows # Provided for your convenience

engine = create_engine('sqlite:///db/lesson.db', echo=True, echo_pool="debug")  
Session = sessionmaker(bind=engine)

__all__ = ['select', 'func', 'Product', 'Order', 'Lineitem',
            'Customer', 'Employee', 'print_record',
            'print_records', 'print_rows', 'Session', 'any_', 'all_', 
            'exists', 'and_', 'or_', 'not_']