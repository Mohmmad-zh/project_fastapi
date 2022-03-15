from app.database import Base
from sqlalchemy import String, Float, Integer, Column, Text, ForeignKey
from sqlalchemy.orm import relationship


class Product(Base): # inherets from Base class
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    price = Column(Float, nullable=False)
    tax = Column(Float)
    owner_id = Column(Integer, ForeignKey("users.id"))


    owner = relationship("User", back_populates="products")

    

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    products = relationship("Product", back_populates="owner")