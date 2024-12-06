from models import *

class Lineitem(Base):
   __tablename__ = "line_items"
   line_item_id = Column(Integer, primary_key=True, autoincrement=True)
   order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)
   product_id = Column(Integer, ForeignKey('products.product_id'), nullable = False)
   quantity = Column(Integer)
   order = relationship("Order", back_populates= "line_items")
   product = relationship("Product", back_populates="line_items")

