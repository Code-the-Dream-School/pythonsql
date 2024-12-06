from models import *

class Customer(Base):
   __tablename__ = 'customers' 
   customer_id = Column(Integer, primary_key = True, autoincrement=True)
   customer_name = Column(String)
   contact = Column(String)
   street = Column(String)
   city = Column(String)
   postal_code = Column(String)
   country = Column(String)
   phone = Column(String)
   orders = relationship("Order", back_populates = "customer")