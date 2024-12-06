from models import *
from sqlalchemy import DateTime
from models.Lineitem import Lineitem

class Order(Base):
   __tablename__ = 'orders'
   order_id = Column(Integer, primary_key=True, autoincrement=True)
   customer_id = Column(Integer,ForeignKey('customers.customer_id'), nullable=False)
   employee_id = Column(Integer, ForeignKey('employees.employee_id'), nullable=False)
   date = Column(DateTime)
   customer = relationship("Customer", back_populates = "orders")
   employee = relationship("Employee", back_populates = "orders")
   line_items = relationship("Lineitem", back_populates = "order")
   products = relationship('Product', secondary=Lineitem.__table__, back_populates = 'orders',
                           overlaps='order,orderdetails,product')
