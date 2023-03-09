"""

 service.py
 the database operations file

"""

from flask import current_app#, jsonify
from sqlalchemy.sql import func
from ..models import db, Client, Order, Product

def get_clients_list(filtration, **kwargs):
    """ Returns list of clients and amount of orders """
    with current_app.app_context():
        if filtration is True:
            data = Client.query.filter(Client.date >= kwargs['date_from'])\
                .filter(Client.date <= kwargs['date_to']).all()
        else:
            data = Client.query.all()
        orders = []
        for item in data:
            count = Order.query.filter(Order.user_id == item.id).all()
            orders.append(len(count))
    return data, orders

"""def get_client_with_filter(model, filter, compare):
    #Returns single client object
    return model.query.filter(filter == compare).first()"""

def get_orders_list(filtration, **kwargs):
    """ Returns list of orders """
    with current_app.app_context():
        if filtration is True:
            data = Order.query.filter(Order.date >= kwargs['date_from'])\
                .filter(Order.date <= kwargs['date_to']).all()
        else:
            data = Order.query.all()
        order = []
        for item in data:
            products=[]
            for i in item.items:
                products.append(i.name)
            order.append(products)
    return data, order

def get_item_with_filter(clas, filter, compare):
    """ Returns single Client/Order/Product object"""
    return clas.query.filter(filter == compare).first()


def get_products_list(filtration, **kwargs):
    """ Returns list of products"""
    with current_app.app_context():
        if filtration is True:
            data = Product.query.filter(Product.cost >= kwargs['price_from'])\
                .filter(Product.cost <= kwargs['price_to']).all()
            print(Product.query.filter(Product.cost >= kwargs['price_from']).all(),\
                  kwargs['price_from'], kwargs['price_to'])
        else:
            data = Product.query.all()
    return data

def commit():
    """ Commits database changes """
    return db.session.commit()

def create_item(model):
    """ Creates a row in database"""
    db.session.add(model)
    commit()
    return 1

def sum_of_orders():
    """ Returns sum of all orders price """
    result = db.session.query(
        func.sum(Order.cost)
    ).scalar()
    print(result)
    return result
