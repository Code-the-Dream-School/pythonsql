from models import *

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
