""" This is the main routes module """
from flask import render_template, url_for, Blueprint, redirect, flash, request
from marshmallow import Schema, fields
from datetime import date
from ..models import Client, Order, db, order_product
from ..service import *
from ..forms import CreateClientForm, CreateOrderForm, CreateProductForm, DeleteItem, Filters
from sqlalchemy import update

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
    form = Filters()
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    print(sum_of_orders())
    if date_from != None and date_to != None:
        data, orders = get_clients_list(True, date_from=date_from, date_to=date_to)
        if data == []:
            flash("No rows found")
    else:
        data, orders = get_clients_list(False)
    return render_template('bp/clients.html', page='client', data=data, orders=orders, len=len(data), form=form)


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
                db.session.add(Client(first_name=form.first_name.data, last_name=form.last_name.data,
                                      email=form.email.data, phone=form.phone.data, date=date.today()))
                db.session.commit()
                return redirect('/clients')
    return render_template('bp/manipulate_client.html', page='client', form=form)


@bp.route('/edit_client/<int:id>', methods=['GET', 'POST'])
def edit_client(id):
    """ Product creation page """
    client = get_item_with_filter(Client, Client.id, id)
    if client == None:
        flash("There's no product with id {}".format(id))
    else:
        form = CreateClientForm(first_name=client.first_name, last_name=client.last_name, email=client.email, phone=client.phone)
        if form.cancel.data:
            return redirect('/clients')
        else:
            if form.validate_on_submit():
                if form.submit.data:
                    client.first_name=form.first_name.data
                    client.last_name=form.last_name.data
                    client.email=form.email.data
                    client.phone=form.phone.data
                    db.session.add(client)
                    db.session.commit()
                    return redirect('/clients')
    return render_template('bp/manipulate_client.html', page='product', form=form)


@bp.route('/delete_client/<int:id>', methods=['GET', 'POST'])
def delete_client(id):
    form = DeleteItem()
    if form.cancel.data:
        return redirect('/orders')
    else:
        if form.validate_on_submit():
            client = get_item_with_filter(Client, Client.id, id)
            print(client)
            db.session.delete(client)
            db.session.commit()
            return redirect('/clients')
    return  render_template('bp/delete_item.html', type="new", form=form, item = "client", id = id)


@bp.route('/orders')
def orders():
    """ The orders page """
    form=Filters()
    items=[]
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    print("date range: ", date_from, date_to)
    if date_from != None and date_to != None:
        data, order = get_orders_list(True, date_from=date_from, date_to=date_to)
        if data == []:
            flash("No rows found")
    else:
        data, order = get_orders_list(False)

    for item in order:
        items.append(', '.join(item))
        #items = ' '.join([str(elem) for elem in item])
    print("items: ",items)
    return render_template('bp/orders.html', page='order', data=data, len=len(data), order=items, form=form)


@bp.route('/new_order', methods=['GET', 'POST'])
def new_order():
    """ Order creation page """
    form = CreateOrderForm()
    if form.cancel.data:
        return redirect('/clients')
    else:
        if form.validate_on_submit():
            full_name = form.name.data
            phone = form.phone.data
            positions = form.order.data
            client = get_item_with_filter(Client, Client.phone, phone)
            if client:
                name = full_name.split(" ")
                order = positions.split(", ")
                print(order)
                cost = 0
                items=[]
                checked = []
                if name[0] == client.first_name and name[1] == client.last_name:
                    available = True
                    for item in order:
                        if item in checked:
                            flash("You can order only 1 unit per product")
                            available = False
                        checked.append(item)
                        print(item, checked)
                        product = get_item_with_filter(Product, Product.name, item)
                        if item not in product.name:
                            flash("No product with name {}".format(item))
                            available = False
                        elif product.amount < 1:
                            flash("You`ve ordered too much or {} is out of stock".format(item))
                            available = False
                        if available == True:
                            cost += product.cost
                            items.append(product)
                            product.amount -= 1
                            commit()
                            create_item(Order(date=form.date.data, user_id=client.id, cost=cost,
                                              address=form.address.data, items=items))

                    return redirect('/orders')
            else:
                flash("No client with this data")
    return render_template('bp/manipulate_order.html', page='order', form=form)


@bp.route('/edit_order/<int:id>', methods=['GET', 'POST'])
def edit_order(id):
    """ Product creation page """
    order = get_item_with_filter(Order, Order.id, id)
    client = get_item_with_filter(Client, Client.id, order.user_id)
    items = [i.name for i in order.items]
    items = ', '.join(items)
    if order == None:
        flash("There's no product with id {}".format(id))
    else:
        form = CreateOrderForm(name=client.first_name+" "+client.last_name, phone=client.phone, order=items, address=order.address,
                                 date=order.date, )
        if form.cancel.data:
            return redirect('/clients')
        else:
            if form.validate_on_submit():
                print("validate")
                name = form.name.data.split(" ")
                phone = form.phone.data
                order_list = form.order.data.split(", ")
                client = get_item_with_filter(Client, Client.phone, phone)
                if client:
                    print('ckient', name)
                    print('order_list',order_list)
                    cost = 0
                    checked=[]
                    if name[0] == client.first_name and name[1] == client.last_name:
                        available = True
                        for item in order_list:
                            if item in checked:
                                flash("You can order only 1 unit per product")
                                available = False
                            checked.append(item)
                            print("Checking: ",item, checked)
                            print(checked[0])

                            product = get_item_with_filter(Product, Product.name, item)
                            print('product', product)
                            if item not in product.name:
                                flash("No product with name {}".format(item))
                                available = False
                            elif product.amount < 1:
                                flash("You`ve ordered too much or {} is out of stock".format(item))
                                available = False
                        if available == True:
                            order.items=[]
                            order.cost=0
                            for item in checked:
                                buf = get_item_with_filter(Product, Product.name, item)
                                order.cost+=buf.cost
                                order.items.append(buf)
                                commit()
                                print("order.items", order.items)
                        return redirect('/orders')
                else:
                    flash("No client with this data")
    return render_template('bp/manipulate_order.html', page='order', form=form)


"""   if available == True:
       cost += product.cost
       order.items.append(product)
       product.amount -= 1
       commit()
       print("Pushing  ",items)
       order.items = items
       commit()
       create_item(Order(date=form.date.data, user_id=client.id, cost=cost,
                             address=form.address.data, items=items))"""

@bp.route('/delete_order/<int:id>', methods=['GET', 'POST'])
def delete_order(id):
    form = DeleteItem()
    if form.cancel.data:
        return redirect('/orders')
    else:
        if form.validate_on_submit():
            order = get_item_with_filter(Order, Order.id, id)
            print(order)
            db.session.delete(order)
            db.session.commit()
            return redirect('/orders')
    return  render_template('bp/delete_item.html', type="new", form=form, item = "order", id = id)


@bp.route('/products')
def products():
    """ The products page """
    form = Filters()
    price_from = request.args.get('price_from')
    price_to = request.args.get('price_to')
    print("price range: ", price_from, price_to)
    if price_from != None and price_to != None:
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
            if product_in_db == None:
                print("Can add")
                create_item(Product(name=name, category=category, cost=cost, amount=amount, year=year))
                return redirect('/products')
    return render_template('bp/manipulate_product.html', page='product', form=form)


@bp.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    """ Product creation page """
    product = get_item_with_filter(Product, Product.id, id)
    if product == None:
        flash("There's no product with id {}".format(id))
    else:
        form = CreateProductForm(name=product.name, category=product.category, year=product.year, cost=product.cost, amount=product.amount,)
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
                    db.session.add(product)
                    db.session.commit()
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
            print(product)
            db.session.delete(product)
            db.session.commit()
            return redirect('/products')
    return  render_template('bp/delete_item.html', type="new", form=form, item = "product", id = id)