from models import *

class Supplier(Base):
   __tablename__ = "suppliers"
   SupplierID = Column(Integer, primary_key=True, autoincrement=True)
   SupplierName = Column(String)
   ContactName = Column(String)
   Address = Column(String)
   City = Column(String)
   PostalCode = Column(String)
   Country = Column(String)
   Phone = Column(String)
   products = relationship("Product", back_populates= "supplier")