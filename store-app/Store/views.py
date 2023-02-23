from Store import app
from flask import render_template, url_for

@app.route('/')
@app.route('/clients')
def clients():
    return render_template('clients.html', page='client')

@app.route('/orders')
def orders():
    return render_template('orders.html', page='order')

@app.route('/products')
def products():
    return render_template('products.html', page='product')

@app.route('/new_client')
def new_client():
    return render_template('new_client.html', page='client')

@app.route('/new_order')
def new_order():
    return render_template('new_order.html', page='order')

@app.route('/new_product')
def new_product():
    return render_template('new_product.html', page='product')