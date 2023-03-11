from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields,validate
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api
from ..service import *

api_bp = Blueprint('api', __name__, template_folder="bp")
api = Api(api_bp)
ma = Marshmallow()
class ClientsList(Resource):
    def get(self):
        clients = get_clients_list(False)
        # print(clients)
        result = clients_schema.dump(clients)
        return result, 200
    def post (self):
        """ The main (clients) page """
        #args = parser.parse_args()
        #return args['task']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        date = request.form['date']
        if not get_items_with_filter(Client, Client.phone, phone):
            if not get_items_with_filter(Client, Client.email, email):
                create_item(Client(first_name=first_name, last_name=last_name, email=email, phone=phone, date=date))
            else:
                return "Client with this email exists", 400
        elif len(phone) > 13 or len(phone) < 13:
            return "Wrong number lenght", 400
        else:
            return "Client with this phone exists", 400
        return "You`ve added a client", 201

class Clients(Resource):
    def get(self, id):
        client = get_item_with_filter(Client, Client.id, id)
        if client == None:
            return "No client with this id", 400
        result = client_schema.dump(client)
        return jsonify(result)
    def put(self, id):
        client = get_item_with_filter(Client, Client.id, id)
        if client == None:
            return ("There's no client with id {}".format(id)), 400
        else:
            resp='hello, '
            keys=client_schema.dump(client).keys()
            a = "keys:"+str( keys)
            #resp+=a
            for item in request.form.keys():
                if item == 'first_name':
                    client.first_name = request.form['first_name']
                elif item == 'last_name':
                    client.first_name = request.form['last_name']
                elif item == 'phone':
                    client.first_name = request.form['phone']
                elif item == 'email':
                    client.first_name = request.form['email']
            edit_item(client)
            result = client_schema.dump(client)
            return result, 200
    def delete(self, id):
        client = get_item_with_filter(Client, Client.id, id)
        if client == None:
            return ("There's no client with id {}".format(id)), 400
        else:
            delete_item(client)
            return "Deleted  user with id={}".format(id), 200

class OrdersList(Resource):
    def get(self):
        orders = get_orders()
        if orders == None:
            return ("There's no orders yet"), 400
        else:
            for item in orders:
                buf = []
                for i in item.products:
                    buf.append(i.name)
                buf = ', '.join(buf)
                item.items = buf
            result = orders_schema.dump(orders)
            return result, 200

    def post(self):
        full_name = request.form['full_name']
        phone = request.form['phone']
        positions = request.form['order']
        client = get_item_with_filter(Client, Client.phone, phone)
        if client and client.first_name + ' ' + client.last_name == full_name:
            name = full_name.split(" ")
            order_list = positions.split(", ")
            if len(order_list) != len(set(order_list)):
                return ("You can order only 1 unit per product"), 400
            cost = 0
            items = []
            checked = []
            if name[0] == client.first_name and name[1] == client.last_name:
                for item in order_list:
                    checked.append(item)
                    product = get_item_with_filter(Product, Product.name, item)
                    if item not in product.name:
                        return "No product with name {}", 400
                    elif product.amount < 1:
                        return "You`ve ordered too much or {} is out of stock", 400
                order = Order(date=request.form['date'], user_id=client.id, cost=cost,
                                  address=request.form['address'], products=items)
                for item in checked:
                    buf = get_item_with_filter(Product, Product.name, item)
                    order.cost += buf.cost
                    order.products.append(buf)
                    buf.amount -= 1
                    commit()
                create_item(order)
                return "Created successfully", 201
        else:
            return "No client with this data", 400

class Orders(Resource):
    def get(self, id):
        order = get_item_with_filter(Client, Client.id, id)
        if order == None:
            return "No order with this id", 400
        result = order_schema.dump(order)
        return jsonify(result)
    def put(self, id):
        order = get_item_with_filter(Order, Order.id, id)
        if order == None:
            return "There's no product with id {}".format(id), 400
        else:
            name = request.form['full_name'].split(" ")
            phone = request.form['phone']
            order_list = request.form['order'].split(", ")
            if len(order_list) != len(set(order_list)):
                return "You can order only 1 unit per product", 400
            client = get_item_with_filter(Client, Client.phone, phone)
            if client == None:
                return "No client with this data", 400
            else:
                cost = 0
                checked = []
                if name[0] == client.first_name and name[1] == client.last_name:
                    for item in order_list:
                        checked.append(item)
                        product = get_item_with_filter(Product, Product.name, item)
                        if item not in product.name:
                            return "No product with name {}", 400
                        elif product.amount < 1:
                            return "You`ve ordered too much or {} is out of stock", 400
                    order.cost = 0
                    order.products = []
                    for item in checked:
                        buf = get_item_with_filter(Product, Product.name, item)
                        order.cost += buf.cost
                        order.products.append(buf)
                    edit_item(order)
                    return "Edited successfully", 200
                else:
                    return "No client with this data", 400
    def delete(self, id):
        order = get_item_with_filter(Order, Order.id, id)
        if order == None:
            return ("There's no order with id {}".format(id)), 400
        else:
            delete_item(order)
            return "Deleted  order with id={}".format(id), 200

class ClientsOrders(Resource):
    def get(self, id):
        orders = get_items_with_filter(Order, Order.user_id, id)
        if orders == None:
            return ("There's no orders yet"), 400
        else:
            result = orders_schema.dump(orders)
            return result, 200

class ProductsList(Resource):
    def get(self):
        products = get_products_list(False)
        if products == None:
            return "There`s no orders yet", 400
        result = products_schema.dump(products)
        return result, 200
    def post (self):
        """ The main (clients) page """
        name = request.form['name']
        category = request.form['category']
        year = request.form['year']
        cost = request.form['cost']
        amount = request.form['amount']
        product_in_db = get_item_with_filter(Product, Product.name, name)
        if product_in_db == None:
            create_item(Product(name=name, category=category, cost=cost, amount=amount, year=year))
            return "You added a product", 201
        else:
            return "A product with this name already exists", 400

class Products(Resource):
    def get(self, id):
        product = get_item_with_filter(Product, Product.id, id)
        if product == None:
            return "No product with this id", 400
        result = product_schema.dump(product)
        return jsonify(result)
    def put(self, id):
        product = get_item_with_filter(Product, Product.id, id)
        if product == None:
            return ("There's no product with this data".format(id)), 400
        else:
            keys=product_schema.dump(product).keys()
            a = "keys:"+str( keys)
            #resp+=a
            for item in request.form.keys():
                if item == 'name':
                    product.name = request.form['name']
                elif item == 'category':
                    product.category = request.form['category']
                elif item == 'year':
                    product.year = request.form['year']
                elif item == 'price':
                    product.price = request.form['price']
                elif item == 'amount':
                    product.amount = request.form['amount']
            edit_item(product)
            result = product_schema.dump(product)
            return result, 200
    def delete(self, id):
        product = get_item_with_filter(Product, Product.id, id)
        if product == None:
            return ("There's no client with id {}".format(id)), 400
        else:
            delete_item(product)
            return "Deleted  user with id={}".format(id), 200


api.add_resource(ClientsList, '/api/clients_list')
api.add_resource(Clients, '/api/client/<int:id>')
api.add_resource(OrdersList, '/api/orders_list')
api.add_resource(ClientsOrders, '/api/orders_list/client/<int:id>')
api.add_resource(Orders, '/api/order/<int:id>')
api.add_resource(ProductsList, '/api/products_list')
api.add_resource(Products, '/api/product/<int:id>')



class ProductSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    cost = fields.Integer()

class OrderSchema(Schema):
    id = fields.Integer()
    user_id = fields.Str()
    cost = fields.Integer()
    address = fields.Str()
    date = fields.Date()
    items = fields.Str()


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

class ProductSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    category = fields.String()
    year = fields.Integer()
    price = fields.Integer()
    amount = fields.Integer()



client_schema=ClientSchema()
clients_schema=ClientSchema(many=True)


order_schema=OrderSchema()
orders_schema=OrderSchema(many=True)

product_schema=ProductSchema()
products_schema=ProductSchema(many=True)