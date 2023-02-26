""" This is the main routes module """
from flask import render_template, url_for, Blueprint, redirect

bp = Blueprint('bp', __name__, template_folder="bp")
@bp.route('/')
@bp.route('/clients')
def clients():
    """ The main (clients) page """
    return render_template('bp/clients.html', page='client')
    # redirect(url_for('bp.orders'))


@bp.route('/orders')
def orders():
    """ The orders page """
    return render_template('bp/orders.html', page='order')


@bp.route('/products')
def products():
    """ The products page """
    return render_template('bp/products.html', page='product')


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
