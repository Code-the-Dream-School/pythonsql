from models import *
from sqlalchemy import types
from models import Lineitem

class Product(Base):
   __tablename__ = "products"
   product_id = Column(Integer, primary_key = True, autoincrement=True)
   product_name = Column(String)
   price = Column(types.FLOAT)
   line_items = relationship("Lineitem", back_populates= 'product', overlaps='products')
   orders = relationship('Order', secondary=Lineitem.__table__, back_populates='products',
                         overlaps='line_items,product,order')
