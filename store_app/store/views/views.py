""" This is the main routes module """
from flask import render_template, Blueprint, redirect, flash, request
from datetime import date
from ..service import *
from ..forms import CreateClientForm, CreateOrderForm, CreateProductForm, DeleteItem, Filters

bp = Blueprint('bp', __name__, template_folder="bp")


@bp.route('/')
@bp.route('/clients')
def clients():
    """ The main (clients) page """
    form = Filters()
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    print(sum_of_orders())
    if date_from is not None and date_to is not None:
        data = get_clients_list(True, date_from=date_from, date_to=date_to)
        if data == []:
            flash("No rows found")
    else:
        data = get_clients_list(False)
    return render_template('bp/clients.html', page='client', data=data, form=form)


@bp.route('/new_client', methods=['GET', 'POST'])
def new_client():
    """ Client creation page """
    form = CreateClientForm()
    if form.cancel.data:
        return redirect('/clients')
    else:
        if form.validate_on_submit():
            email=form.email.data
            phone=form.phone.data
            if Client.query.filter(Client.email == email).first():
                flash("Email already in use")
            elif Client.query.filter(Client.phone == phone).first():
                flash("Phone number already in use")
            else:
                edit_item(Client(first_name=form.first_name.data, last_name=form.last_name.data,
                                email=form.email.data, phone=form.phone.data, date=date.today()))
                return redirect('/clients')
    return render_template('bp/manipulate_client.html', page='client', form=form)


@bp.route('/edit_client/<int:id>', methods=['GET', 'POST'])
def edit_client(id):
    """ Product creation page """
    client = get_item_with_filter(Client, Client.id, id)
    if client is None:
        flash("There's no product with id {}".format(id))
        return redirect('/clients')
    else:
        form = CreateClientForm(first_name=client.first_name, last_name=client.last_name,\
                                email=client.email, phone=client.phone)
        if form.cancel.data:
            return redirect('/clients')
        else:
            if form.validate_on_submit():
                if form.submit.data:
                    client.first_name=form.first_name.data
                    client.last_name=form.last_name.data
                    client.email=form.email.data
                    client.phone=form.phone.data
                    edit_item(client)
                    return redirect('/clients')
    return render_template('bp/manipulate_client.html', page='product', form=form)


@bp.route('/delete_client/<int:id>', methods=['GET', 'POST'])
def delete_client(id):
    """ Delete confirm page """
    form = DeleteItem()
    if form.cancel.data:
        return redirect('/orders')
    else:
        if form.validate_on_submit():
            client = get_item_with_filter(Client, Client.id, id)
            if client is None:
                flash("There's no client with id {}".format(id))
                return redirect('/clients')
            delete_item(client)
            return redirect('/clients')
    return  render_template('bp/delete_item.html', type="new", form=form, item = "client", id = id)


@bp.route('/orders')
def orders():
    """ The orders page """
    form=Filters()
    items=[]
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    if date_from is not None and date_to is not None:
        data, order = get_orders_list(True, date_from=date_from, date_to=date_to)
        if data == []:
            flash("No rows found")
    else:
        data, order = get_orders_list(False)

    for item in order:
        items.append(', '.join(item))
    return render_template('bp/orders.html', page='order', data=data, len=len(data), order=items, form=form)


@bp.route('/new_order', methods=['GET', 'POST'])
def new_order():
    """ Order creation page """
    form = CreateOrderForm()
    if form.cancel.data:
        return redirect('/orders')
    else:
       if form.validate_on_submit():
            full_name = form.name.data
            phone = form.phone.data
            positions = form.order.data
            client = get_item_with_filter(Client, Client.phone, phone)
            if client and client.first_name+' '+client.last_name == full_name:
                name = full_name.split(" ")
                order_list = positions.split(", ")
                available = True
                if len(order_list) != len(set(order_list)):
                    flash("You can order only 1 unit per product")
                    available=False

                cost = 0
                items=[]
                checked = []
                if name[0] == client.first_name and name[1] == client.last_name:

                    for item in order_list:
                        checked.append(item)
                        product = get_item_with_filter(Product, Product.name, item)
                        validate_order(item, product)

                    if available is True:
                        order = Order(date=form.date.data, user_id=client.id, cost=cost,
                                              address=form.address.data, products=items)

                        for item in checked:
                            buf = get_item_with_filter(Product, Product.name, item)
                            order.cost += buf.cost
                            order.products.append(buf)
                            buf.amount-=1
                            commit()
                        create_item(order)
            else:
                flash("No client with this data")
            return redirect('/orders')
    return render_template('bp/manipulate_order.html', page='order', form=form)


@bp.route('/edit_order/<int:id>', methods=['GET', 'POST'])
def edit_order(id):
    """ Product creation page """
    order = get_item_with_filter(Order, Order.id, id)
    if order is None:
        flash("There's no order with id {}".format(id))
        return redirect('/orders')
    client = get_item_with_filter(Client, Client.id, order.user_id)

    if client is None:
        flash("There's no client with id {}".format(id))
        return redirect('/orders')
    items = [i.name for i in order.products]
    items = ', '.join(items)
    if order is None:
        flash("There's no product with id {}".format(id))
    else:
        form = CreateOrderForm(name=client.first_name+" "+client.last_name, phone=client.phone,\
                               order=items, address=order.address, date=order.date)
        if form.cancel.data:
            return redirect('/orders')
        else:
            if form.validate_on_submit():
                name = form.name.data.split(" ")
                phone = form.phone.data
                order_list = form.order.data.split(", ")
                if len(order_list) != len(set(order_list)):
                    flash("You can order only 1 unit per product")

                client = get_item_with_filter(Client, Client.phone, phone)
                if client:
                    checked=[]
                    if name[0] == client.first_name and name[1] == client.last_name:
                        available = True

                        for item in order_list:
                            checked.append(item)
                            product = get_item_with_filter(Product, Product.name, item)
                            available = validate_order(item, product)

                        if available is True:
                            order.cost=0
                            order.products=[]
                            for item in checked:
                                buf = get_item_with_filter(Product, Product.name, item)
                                order.cost+=buf.cost
                                order.products.append(buf)
                            order.date=form.date.data
                            edit_item(order)

                        else:
                            return redirect('/edit_order/'+str(id))
                        return redirect('/orders')
                else:
                    flash("No client with this data")
    return render_template('bp/manipulate_order.html', page='order', form=form)


@bp.route('/delete_order/<int:id>', methods=['GET', 'POST'])
def delete_order(id):
    """ The delete order confirm """
    form = DeleteItem()
    if form.cancel.data:
        return redirect('/orders')
    else:
        if form.validate_on_submit():
            order = get_item_with_filter(Order, Order.id, id)
            if order is None:
                flash("There's no order with id {}".format(id))
                return redirect('/orders')
            delete_item(order)
            return redirect('/orders')
    return  render_template('bp/delete_item.html', type="new", form=form, item = "order", id = id)


@bp.route('/products')
def products():
    """ The products page """
    form = Filters()
    price_from = request.args.get('price_from')
    price_to = request.args.get('price_to')
    if price_from is not None and price_to is not None:
        data = get_products_list(True, price_from=price_from, price_to=price_to)
        if data == []:
            flash("No rows found")
    else:
        data = get_products_list(False)
    return render_template('bp/products.html', page='product', data=data, len=len(data), form=form)


@bp.route('/new_product', methods=['GET', 'POST'])
def new_product():
    """ Product creation page """
    form = CreateProductForm()
    if form.cancel.data:
        return redirect('/clients')
    else:
        if form.validate_on_submit():
            name = form.name.data
            category = form.category.data
            year = form.year.data
            cost=form.cost.data
            amount = form.amount.data
            product_in_db = get_item_with_filter(Product, Product.name, name)
            if product_in_db is None:
                create_item(Product(name=name, category=category, cost=cost,\
                                    amount=amount, year=year))
                return redirect('/products')
            else:
                flash("A product with this name already exists")
    return render_template('bp/manipulate_product.html', page='product', form=form)


@bp.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    """ Product creation page """
    product = get_item_with_filter(Product, Product.id, id)
    if product is None:
        flash("There's no product with id {}".format(id))
        return redirect('/products')
    else:
        form = CreateProductForm(name=product.name, category=product.category,\
                                 year=product.year, cost=product.cost, amount=product.amount,)
        if form.cancel.data:
            return redirect('/clients')
        else:
            if form.validate_on_submit():
                if form.submit.data:
                    product.name=form.name.data
                    product.category=form.category.data
                    product.cost=form.cost.data
                    product.amount=form.amount.data
                    product.year=form.year.data
                    edit_item(product)
                    return redirect('/products')
    return render_template('bp/manipulate_product.html', page='product', form=form)


@bp.route('/delete_product/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    form = DeleteItem()
    if form.cancel.data:
        return redirect('/orders')
    else:
        if form.validate_on_submit():
            product = get_item_with_filter(Product, Product.id, id)
            if product is None:
                flash("There's no product with id {}".format(id))
                return redirect('/products')
            delete_item(product)
            return redirect('/products')
    return  render_template('bp/delete_item.html', type="new", form=form, item = "product", id = id)


def validate_order(item, product):
    if item not in product.name:
        flash("No product with name {}".format(item))
        return False
    elif product.amount < 1:
        flash("You`ve ordered too much or {} is out of stock".format(item))
        return False
    return True
