from sqlalchemy import Column, Integer, String, Date, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, declarative_base

db = SQLAlchemy()

class Link(db.Model):
    __tablename__ = 'link'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))


class Client(db.Model):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(40), nullable=False)
    last_name = Column(String(40), nullable=False)
    email = Column(String(80), nullable=False)
    phone = Column(String(13), nullable=False)
    date = Column(Date, nullable=True)
    orders = db.relationship('Order', backref='clients',
                                lazy='subquery')


class Order(db.Model):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('clients.id'))
    date = Column(Date, nullable=False)
    cost = Column(Integer, nullable=False)
    address = Column(String(160), nullable=False)
    products = relationship('Product', secondary = 'link', lazy='subquery')


class Product(db.Model):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    cost = Column(Integer, nullable=False)
    category = Column(String(20), nullable=False)
    year = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    orders = relationship(Order,secondary='link',lazy='subquery',overlaps="products")
