from sqlalchemy import MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase
class Base(DeclarativeBase):
    pass

__all__ = ['Base', 'Column', 'Integer', 'String', 'relationship', 'ForeignKey']

from .Customer import Customer
from .Category import Category
from .Employee import Employee
from .Order import Order
from .OrderDetail import OrderDetail
from .Product import Product
from .Shipper import Shipper
from .Supplier import Supplier

target_metadata = Base.metadata