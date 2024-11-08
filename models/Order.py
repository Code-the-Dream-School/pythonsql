from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column
from models import *
from models.OrderDetail import OrderDetail

class Order(Base):
   __tablename__ = 'orders'
   OrderID = Column(Integer, primary_key=True, autoincrement=True)
   CustomerID = Column(Integer,ForeignKey('customers.CustomerID'), nullable=False)
   EmployeeID = Column(Integer, ForeignKey('employees.EmployeeID'), nullable=False)
   OrderDate = Column(String)
   ShipperID = Column(Integer, ForeignKey('shippers.ShipperID'), nullable=False)
   customer = relationship("Customer", back_populates = "orders")
   employee = relationship("Employee", back_populates = "orders")
   orderdetails = relationship("OrderDetail", back_populates = "order")
   shipper = relationship("Shipper", back_populates="orders")
   products = relationship('Product', secondary=OrderDetail.__table__, back_populates = 'orders',
                           overlaps='order,orderdetails,product')
