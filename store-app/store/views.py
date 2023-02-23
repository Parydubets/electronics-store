""" This is the main routes module """
from flask import render_template, url_for
from store import app


@app.route('/')
@app.route('/clients')
def clients():
    """ The main (clients) page """
    return render_template('clients.html', page='client')

@app.route('/orders')
def orders():
    """ The orders page """
    return render_template('orders.html', page='order')

@app.route('/products')
def products():
    """ The products page """
    return render_template('products.html', page='product')

@app.route('/new_client')
def new_client():
    """ Client creation page """
    return render_template('new_client.html', page='client')

@app.route('/new_order')
def new_order():
    """ Order creation page """
    return render_template('new_order.html', page='order')

@app.route('/new_product')
def new_product():
    """ Product creation page """
    return render_template('new_product.html', page='product')
