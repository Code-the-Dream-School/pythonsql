from models import *

class Shipper(Base):
   __tablename__ = 'shippers'
   ShipperID = Column(Integer, primary_key=True)
   ShipperName = Column(String)
   Phone = Column(String)
   orders = relationship("Order", back_populates = "shipper")