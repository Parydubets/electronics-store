from flask import current_app, jsonify
from ..models import db, Client, Order, Product

def get_clients_list():
    with current_app.app_context():
        data = Client.query.all()
        orders = []
        for item in data:
            print("items: ", len(item.orders.all()))
            count = Order.query.filter(Order.user_id == item.id).all()
            orders.append(len(count))
    return data, orders

def get_orders_list():
    with current_app.app_context():
        data = Order.query.all()
        order = []
        for item in data:
            products=[]
            for i in item.items:
                products.append(i.name)
            order.append(products)
    return data, order

def get_products_list():
    with current_app.app_context():
        data = Product.query.all()
        for item in data:
            print(item.id)
    return data
