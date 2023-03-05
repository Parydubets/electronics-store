""" This is the main routes module """
from flask import render_template, url_for, Blueprint, redirect
from marshmallow import Schema, fields
from ..models import Client, Order, db
from ..service import *

bp = Blueprint('bp', __name__, template_folder="bp")


class ClientSchema(Schema):
    id = fields.Str()
    first_name = fields.Str()

class OrderSchema(Schema):
    id = fields.Str()
    cost = fields.Str()

@bp.route('/')
@bp.route('/clients')
def clients():
    """ The main (clients) page """
    data, orders = get_clients_list()
    return render_template('bp/clients.html', page='client', data=data, orders=orders, len=len(data))
    # redirect(url_for('bp.orders'))

"""
    print(resp[1].id)
    print(resp[1].first_name)
    print(resp[1].last_name)
    {% for item in data %}
                    <tr>
                        <td>item.id</td>
                        <td>item.first_name</td>
                        <td>item.last_name</td>
                        <td>item.email</td>
                        <td>item.phone</td>
                        <td>item.orders</td>
                        <td>item.date</td>
                        <td class="edit-row"><a href="#"><i class="fa-solid fa-trash-can"></i></a><a href="edit_client.html"><i class="fa-solid fa-gear"></i></a></td>
                    {% endfor %}"""
@bp.route('/orders')
def orders():
    """ The orders page """
    data, order = get_orders_list()
    items=[]
    for item in order:
        items.append(' '.join(item))
        #items = ' '.join([str(elem) for elem in item])
    print("items: ",items)
    return render_template('bp/orders.html', page='order', data=data, len=len(data), order=items)


@bp.route('/products')
def products():
    """ The products page """
    data = get_products_list()
    return render_template('bp/products.html', page='product', data=data, len=len(data))


@bp.route('/new_client')
def new_client():
    """ Client creation page """
    return render_template('bp/new_client.html', page='client')


@bp.route('/new_order')
def new_order():
    """ Order creation page """
    return render_template('bp/new_order.html', page='order')


@bp.route('/new_product')
def new_product():
    """ Product creation page """
    return render_template('bp/new_product.html', page='product')
