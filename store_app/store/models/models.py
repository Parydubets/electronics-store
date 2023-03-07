from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
order_product = db.Table(
    'order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id')),
)


class Client(db.Model):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(40), nullable=False)
    last_name = Column(String(40), nullable=False)
    email = Column(String(80), nullable=False)
    phone = Column(String(13), nullable=False)
    date = Column(Date, nullable=True)
    orders = db.relationship('Order', backref='clients',
                                lazy='dynamic')


class Order(db.Model):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey('clients.id'))
    date = Column(Date, nullable=False)
    cost = Column(Integer, nullable=False)
    address = Column(String(160), nullable=False)
    items = db.relationship('Product', secondary=order_product,
                           backref=db.backref('orders', lazy='subquery'))

class Product(db.Model):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), nullable=False)
    cost = Column(Integer, nullable=False)
    category = Column(String(20), nullable=False)
    year = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)




