from models import *

class Category(Base):
   __tablename__ = "categories"
   CategoryID = Column(Integer, primary_key=True)
   CategoryName = Column(String)
   Description = Column(String)
   products = relationship("Product", back_populates="category")
   