""" The rest api file """
from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields,validate
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api
from ..service import get_clients_list, get_items_with_filter, create_item, delete_item,\
                    get_orders, get_item_with_filter, edit_item, get_products_list,  \
                    sum_of_orders, sum_of_client_orders, Order, Client, Product

api_bp = Blueprint('api', __name__, template_folder="bp")
api = Api(api_bp)
ma = Marshmallow()
class ClientsList(Resource):
    """ The clients list class """
    def get(self):
        """ Get all clients """
        clients = get_clients_list(False)
        # print(clients)
        result = clients_schema.dump(clients)
        return result, 200
    def post (self):
        """ Creat a new client """
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        date = request.form['date']
        if not get_items_with_filter(Client, Client.phone, phone):
            if len(phone)>13 or len(phone)<13:
                return "Wrong number lenght", 400
            if not get_items_with_filter(Client, Client.email, email):
                create_item(Client(first_name=first_name, last_name=last_name,\
                                   email=email, phone=phone, date=date))
            else:
                return "Client with this email exists", 400
        elif get_items_with_filter(Client, Client.phone, phone):
            return "Client with this phone exists", 400
        return "You`ve added a client", 201

class Clients(Resource):
    """ The Client manipulation class """
    def get(self, id):
        """
        Get client by id

        Form parameters:
            id (int)

        Returns:
            Message, status code
        """
        client = get_item_with_filter(Client, Client.id, id)
        if client is None:
            return "No client with this id", 400
        result = client_schema.dump(client)
        return jsonify(result)
    def put(self, id):
        """
         Edit client by id

        Form parameters (optional):
            first_name (str)
            last_name (str)
            phone (str, 13 characters long)
            last_name (str)

        Returns:
            Message, status code
         """
        client = get_item_with_filter(Client, Client.id, id)
        if client is None:
            return f"There's no client with id {id}", 400
        for item in request.form.keys():
            if item == 'first_name':
                client.first_name = request.form['first_name']
            elif item == 'last_name':
                client.last_name = request.form['last_name']
            elif item == 'phone':
                phone = request.form['phone']
                if len(phone)>13 or len(phone)<13:
                    return 'Invalid phone number', 400
                client.phone = phone
            elif item == 'email':
                if get_items_with_filter(Client, Client.email, request.form['email']):
                    return 'Client with this email already exists', 400
                client.email = request.form['email']
        edit_item(client)
        result = client_schema.dump(client)
        return result, 200
    def delete(self, id):
        """
        Edit client by id

        Form parameters:
            id (int)

        Returns:
            Message, status code
        """
        client = get_item_with_filter(Client, Client.id, id)
        if client is None:
            return f"There's no client with id {id}", 400
        delete_item(client)
        return f"Deleted  user with id={id}", 200

class OrdersList(Resource):
    """ The order list manipulation class """
    def get(self):
        """ Get all orders """
        orders = get_orders()
        if orders is None:
            return ("There's no orders yet"), 400
        for item in orders:
            buf = []
            for i in item.products:
                buf.append(i.name)
            buf = ', '.join(buf)
            item.items = buf
        result = orders_schema.dump(orders)
        return result, 200

    def post(self):
        """
        Create new order

        Form parameters:
            full_name (str)
            phone (str, 13 characters long)
            order (str)
            address (str)
            date (date, <yyyy-mm-dd> )

        Returns:
            Message, status code
        """
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
                    if product is None:
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
                create_item(order)
                return "Created successfully", 201
        else:
            return "No client with this data", 400

class Orders(Resource):
    """ The orders manipulation class """
    def get(self, id):
        """
        Get order by id

        Form parameters:
            id (int)

        Returns:
            Message, status code
        """
        order = get_item_with_filter(Order, Order.id, id)
        if order is None:
            return "No order with this id", 400
        result = order_schema.dump(order)
        return result, 200
    def put(self, id):
        """
        Edit order by id

        Form parameters (optional):
            full_name (str)
            phone (str, 13 characters long)
            order (str)
            address (str)
            date (date, <yyyy-mm-dd> )

        Returns:
            Message, status code
        """
        order = get_item_with_filter(Order, Order.id, id)
        if order is None:
            return f"There's no product with id {id}", 400
        else:
            name = request.form['full_name'].split(" ")
            phone = request.form['phone']
            order_list = request.form['order'].split(", ")
            if len(order_list) != len(set(order_list)):
                return "You can order only 1 unit per product", 400
            client = get_item_with_filter(Client, Client.phone, phone)
            if client is None:
                return "No client with this data", 400
            else:
                checked = []
                if name[0] == client.first_name and name[1] == client.last_name:
                    for item in order_list:
                        checked.append(item)
                        product = get_item_with_filter(Product, Product.name, item)
                        if item not in product.name:
                            return f"No product with name {product.name}", 400
                        elif product.amount < 1:
                            return f"You`ve ordered too much or {product.name} is out of stock", 400
                    order.cost = 0
                    order.products = []
                    for item in checked:
                        buf = get_item_with_filter(Product, Product.name, item)
                        order.cost += buf.cost
                        order.products.append(buf)
                    order.date = request.form['date']
                    edit_item(order)
                    return "Edited successfully", 200
                else:
                    return "No client with this data", 400
    def delete(self, id):
        """ Delete client by id """
        order = get_item_with_filter(Order, Order.id, id)
        if order is None:
            return f"There's no order with id {id}", 400
        delete_item(order)
        return f"Deleted  order with id={id}", 200

class ClientsOrders(Resource):
    """
    Get client`s orders by id

    Form parameters:
        id (int)

    Returns:
        Message, status code
    """
    def get(self, id):
        orders = get_items_with_filter(Order, Order.user_id, id)
        client = get_item_with_filter(Client, Client.id, id)
        if orders is None:
            return "There's no orders yet", 400
        if client is None:
            return "Wrong client id", 400
        result = orders_schema.dump(orders)
        return result, 200

class ProductsList(Resource):
    """ The products list manipulation class """

    def get(self):
        """ Get all products """
        products = get_products_list(False)
        if products == None:
            return "There`s no orders yet", 400
        result = products_schema.dump(products)
        return result, 200
    def post (self):
        """
        Create new product

        Form parameters:
            name (str)
            category (str)
            year (int)
            cost (int)
            amount (int)

        Returns:
            Message, status code
        """
        name = request.form['name']
        category = request.form['category']
        year = request.form['year']
        cost = request.form['cost']
        amount = request.form['amount']
        product_in_db = get_item_with_filter(Product, Product.name, name)
        if product_in_db is None:
            create_item(Product(name=name, category=category, cost=cost, amount=amount, year=year))
            return "You added a product", 201
        return "A product with this name already exists", 400

class Products(Resource):
    """ The products manipulation class """
    def get(self, id):
        """
        Get product by id

        Form parameters:
            id (int)

        Returns:
            Message, status code
        """
        product = get_item_with_filter(Product, Product.id, id)
        if product is None:
            return "No product with this id", 400
        result = product_schema.dump(product)
        return jsonify(result)
    def put(self, id):
        """
        Edit product by id

        Form parameters (optional):
            name (str)
            category (str)
            year (int)
            cost (int)
            amount (int)

        Returns:
            Message, status code
        """
        product = get_item_with_filter(Product, Product.id, id)
        if product is None:
            return f"There's no product with this data", 400
        else:
            keys=product_schema.dump(product).keys()
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
        """ Delete product by id """
        product = get_item_with_filter(Product, Product.id, id)
        if product is None:
            return f"There's no client with id {id}", 400
        delete_item(product)
        return "Deleted  user with id={id}", 200


class AllOrdersSum(Resource):
    """ The sum of orders class """
    def get(self):
        """ Get sum of all orders """
        return str(sum_of_orders()), 200

class ClientOrdersSum(Resource):
    """ The sum of orders class """
    def get(self, id):
        """ Get sum of client's all orders """
        if sum_of_client_orders(id) is None:
            return "No client with this id", 400
        return str(sum_of_client_orders(id)), 200


api.add_resource(ClientsList, '/api/clients_list')
api.add_resource(Clients, '/api/client/<int:id>')
api.add_resource(OrdersList, '/api/orders_list')
api.add_resource(ClientsOrders, '/api/orders_list/client/<int:id>')
api.add_resource(Orders, '/api/order/<int:id>')
api.add_resource(ProductsList, '/api/products_list')
api.add_resource(Products, '/api/product/<int:id>')
api.add_resource(AllOrdersSum, '/api/orders/sum')
api.add_resource(ClientOrdersSum, '/api/client/<int:id>/sum')



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
