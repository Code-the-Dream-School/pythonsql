from sqlalchemy import MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase
class Base(DeclarativeBase):
    pass

__all__ = ['Base', 'Column', 'Integer', 'String', 'relationship', 'ForeignKey']

from .Customer import Customer
from .Employee import Employee
from .Order import Order
from .Lineitem import Lineitem
from .Product import Product

target_metadata = Base.metadata