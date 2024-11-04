from models import *
from sqlalchemy import types

class Product(Base):
   __tablename__ = "products"
   ProductID = Column(Integer, primary_key = True, autoincrement=True)
   ProductName = Column(String)
   SupplierID = Column(Integer, ForeignKey("suppliers.SupplierID"), nullable=False)
   CategoryID = Column(Integer, ForeignKey("categories.CategoryID"), nullable=False)
   Unit = Column(String)
   Price = Column(types.FLOAT)
   supplier = relationship("Supplier", back_populates= "products")
   category = relationship("Category", back_populates= "products")
   orderdetails = relationship("OrderDetail", back_populates= 'product')
