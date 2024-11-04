from models import *

class Customer(Base):
   __tablename__ = 'customers' 
   CustomerID = Column(Integer, primary_key = True, autoincrement=True)
   CustomerName = Column(String)
   ContactName = Column(String)
   Address = Column(String)
   City = Column(String)
   PostalCode = Column(String)
   Country = Column(String)
   orders = relationship("Order", back_populates = "customer")