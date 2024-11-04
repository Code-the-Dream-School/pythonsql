from models import *
from sqlalchemy.ext.hybrid import hybrid_property

class Employee(Base):
   __tablename__ = 'employees'
   EmployeeID = Column(Integer, primary_key=True, autoincrement=True)
   LastName = Column(String)
   FirstName = Column(String)
   BirthDate = Column(String)
   Photo = Column(String)
   Notes = Column(String)
   @hybrid_property
   def FullName(self):
      return self.FirstName + ' ' + self.LastName
   orders = relationship("Order", back_populates = "employee")
