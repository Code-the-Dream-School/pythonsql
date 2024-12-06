from models import *
from sqlalchemy.ext.hybrid import hybrid_property

class Employee(Base):
   __tablename__ = 'employees'
   employee_id = Column(Integer, primary_key=True, autoincrement=True)
   first_name = Column(String)
   last_name = Column(String)
   phone = Column(String)
   @hybrid_property
   def full_name(self):
      return self.FirstName + ' ' + self.LastName
   orders = relationship("Order", back_populates = "employee")
