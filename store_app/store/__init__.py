""" The app initialization file """
import os
from flask import Flask, Blueprint
from flask_migrate import Migrate, init

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config.from_mapping(
            SECRET_KEY='somerandomkey',
            #DATABASE=os.path.join(app.instance_path, 'store.sqlite'),
            #SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir, 'store.db'),
            SQLALCHEMY_DATABASE_URI='mysql://root@127.0.0.1:3306/store',
    )

    #db_seed()
    if test_config is None:
            # load the instance config, if it exists, when not testing
            app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

        # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .views import bp
    from .models import db, Client, Product, Order,order_product
    db.init_app(app)
    app.register_blueprint(bp)

    migrate = Migrate(app, db, directory='store/migrations')
    @app.cli.command('seed')
    def seed():
        with app.app_context():
            user1 = Client(first_name="Peter", last_name="Parker", email="spiderman@gmail.com",
                           phone="+12345612345", date="2023-01-18")
            user2 = Client(first_name="Joel", last_name="Miller", email="thelastjoel@gmail.com",
                           phone="+12323232323", date="2023-02-03")
            user3 = Client(first_name="Johnny", last_name="Silverhand", email="samurai@gmail.com",
                           phone="+12077207720", date="2023-08-20")
            db.session.add(user1)
            db.session.add(user2)
            db.session.add(user3)
            product1=Product(name="Smartphone Q2", cost=200, category="Phones", year=2022, amount=25)
            product2=Product(name="Laptop SM234", cost=1150, category="Laptops", year=2022, amount=13)
            product3=Product(name="Smartphone BM3", cost=240, category="Phones", year=2023, amount=31)
            db.session.add(product1)
            db.session.add(product2)
            db.session.add(product3)
            order1 = Order( date="2023-01-30", user_id=1, cost=250,
                            address="20 Ingram Street, NY, NY, USA")
            order2 = Order( date="2023-02-11", user_id=2, cost=500,
                            address="15215 Thatcher Dr, Austin, Texas, USA")
            order3 = Order( date="2023-08-20", user_id=3, cost=120,
                            address="1205 Haddox Ct, Cpllege Station, Texas. USA")
            db.session.add(order1)
            db.session.add(order2)
            db.session.add(order3)
            db.session.commit()
            ord_pr1 = order_product.insert().values(order_id=1, product_id=1)
            ord_pr2 = order_product.insert().values(order_id=1, product_id=2)
            ord_pr3 = order_product.insert().values(order_id=2, product_id=3)
            ord_pr4 = order_product.insert().values(order_id=3, product_id=2)
            db.session.execute(ord_pr1)
            db.session.execute(ord_pr2)
            db.session.execute(ord_pr3)
            db.session.execute(ord_pr4)
            db.session.commit()
            print("Seeded successfully")

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    return app
#mysql://root:admin@localhost:3306/store