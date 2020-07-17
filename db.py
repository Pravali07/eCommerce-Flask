from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from flask_login import UserMixin

Base=declarative_base()

class Products(Base,UserMixin):
	__tablename__="products"
	id = Column(Integer,primary_key=True)
	image = Column(BLOB,nullable=False)
	description = Column(String(500),nullable=False)
	name = Column(String(30),nullable=False)
	price = Column(Integer,nullable=False)
	tax = Column(Integer,nullable=False)
	inCart = Column(Boolean, nullable=False)
# class Login(Base,UserMixin):
# 	__tablename__="loginDetails"
# 	id = Column(Integer,primary_key=True)
# 	username = Column(String(50),nullable=False)
# 	email = Column(String(50),nullable=False)
# 	password = Column(String(50),nullable=False)

engine=create_engine('sqlite:///product.db')
Base.metadata.create_all(engine)
print("Database created successfully")


