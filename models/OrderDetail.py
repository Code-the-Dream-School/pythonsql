from models import *

class OrderDetail(Base):
   __tablename__ = "orderdetails"
   OrderDetailID = Column(Integer, primary_key=True, autoincrement=True)
   OrderID = Column(Integer, ForeignKey('orders.OrderID'), nullable=False)
   ProductID = Column(Integer, ForeignKey('products.ProductID'), nullable = False)
   Quantity = Column(Integer)
   order = relationship("Order", back_populates= "orderdetails")
   product = relationship("Product", back_populates="orderdetails")
   