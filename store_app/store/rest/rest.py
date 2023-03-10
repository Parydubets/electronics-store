from flask import Blueprint, jsonify, request
from flask import current_app as app
from marshmallow import Schema, fields,validate
from flask_marshmallow import Marshmallow
from ..models import Client, Order, db
from ..service import *


api = Blueprint('api', __name__, template_folder="bp")

ma = Marshmallow()
"""with app.app_context():
    print("-------------------------------------------------------------")
    print(current_app)
    print("-------------------------------------------------------------")"""

class ProductSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    cost = fields.Integer()

class OrderSchema(Schema):
    id = fields.Str()
    user_id = fields.Str()
    cost = fields.Integer()
    address = fields.Str()
    date = fields.Date()
    items = fields.List(fields.Nested(ProductSchema))


class ClientSchema(Schema):
    id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    email = fields.String()
    phone = fields.String(validate=validate.Length(min=13, max=13))
    date = fields.Date()
    order = fields.Nested(OrderSchema)
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'date', 'order')



client_schema=ClientSchema()
clients_schema=ClientSchema(many=True)


order_schema=OrderSchema()
orders_schema=OrderSchema(many=True)
@api.route("/api/hello")
def hello():
    return jsonify("Hello, World!")

@api.route('/api/clients')
def clients():
    """ The main (clients) page """
    clients = get_clients_list(False)
    #print(clients)
    result=clients_schema.dump(clients)
    return jsonify(result)


@api.route('/api/clients/add', methods=['POST'])
def clients_add():
    """ The main (clients) page """
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone = request.form['phone']
    date = request.form['date']
    if not get_items_with_filter(Client, Client.phone, phone):
        if not get_items_with_filter(Client, Client.email, email):
            create_item(Client(first_name=first_name, last_name=last_name, email=email, phone=phone, date=date))
        else:
            return jsonify("Client with this email exists"), 400
    elif len(phone)>13 or len(phone)<13:
        return jsonify("Wrong number lenght"), 400
    else:
        return jsonify("Client with this phone exists"), 400
    return jsonify("You added a client"), 201

@api.route('/api/clients/<int:id>')
def client(id):
    """ The main (clients) page """
    client = get_item_with_filter(Client, Client.id, id)
    print(client)
    result=client_schema.dump(client)
    return jsonify(result)

@api.route('/api/clients/orders/<int:id>')
def client_orders(id):
    """ The main (clients) page """
    orders = get_items_with_filter(Order, Order.user_id, id)
    noone= []
    print(orders)
    if orders == []:
        return jsonify("No orders from client with id={}".format(id)), 400
    result=orders_schema.dump(orders)
    return jsonify(result)


@api.route('/api/orders')
def orders():
    """ The main (clients) page """
    orders = get_orders_list(False)
    orders = get_products()

        #orders[0][i].items=orders[1][i]
    result=orders_schema.dump(orders)
    return jsonify(result)