""" The app initialization file """
import os
import logging
import logging.handlers
from flask import Flask, render_template
from flask_migrate import Migrate
from .views import bp
from .rest import api_bp
from .models import db, Client, Product, Order


def create_app(test_config=None):
    """ The store app creation """
    app = Flask(__name__, instance_relative_config=True)
    handler = logging.handlers.RotatingFileHandler('store.log', maxBytes=1024 * 1024)
    logging.getLogger('werkzeug').setLevel(logging.DEBUG)
    logging.getLogger('werkzeug').addHandler(handler)
    app.config.from_mapping(
            SECRET_KEY='2O9VsppcnbkZkQrWklfUnw',
            SQLALCHEMY_DATABASE_URI='mysql://root@127.0.0.1:3306/store',
            #SQLALCHEMY_DATABASE_URI='mysql://root:admin@localhost:3306/store',
    )

    def set_test(test_config):
        if test_config is None:
            app.config.from_pyfile("config.py", silent=True)
        else:
            app.config.update(test_config)

        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass

    set_test(test_config)

    db.init_app(app)
    app.register_blueprint(bp)
    app.register_blueprint(api_bp)

    migrate = Migrate(app, db, directory='store/migrations')

    @app.cli.command('seed')
    def seed():
        with app.app_context():
            client1=Client(first_name="Peter", last_name="Parker", email="spiderman@gmail.com",
                                   phone="+123456123450", date="2023-01-18")
            client2=Client(first_name="Joel", last_name="Miller", email="thelastjoel@gmail.com",
                                   phone="+123232323230", date="2023-02-03")
            client3=Client(first_name="Johnny", last_name="Silverhand", email="samurai@gmail.com",
                                   phone="+120772077200", date="2023-08-20")
            prod1=Product(name="Smartphone Q2", cost=200, category="Phones",
                                 year=2022, amount=25)
            prod2=Product(name="Laptop SM234", cost=1150, category="Laptops",
                                 year=2022, amount=13)
            prod3=Product(name="Smartphone BM3", cost=240, category="Phones",
                                 year=2023, amount=31)
            db.session.add(prod1)
            db.session.add(prod2)
            db.session.add(prod3)
            ord1=Order( date="2023-01-30", user_id=1, cost=1350,
                                    address="20 Ingram Street, NY, NY, USA")
            ord2=Order( date="2023-02-11", user_id=2, cost=240,
                                    address="15215 Thatcher Dr, Austin, Texas, USA")
            ord3=Order( date="2023-08-20", user_id=3, cost=1150,
                                    address="1205 Haddox Ct, Cpllege Station, Texas. USA")
            ord1.products.append(prod1)
            ord1.products.append(prod2)
            client1.orders.append(ord1)
            db.session.add(ord1)
            db.session.add(client1)
            db.session.commit()
            ord2.products.append(prod3)
            client2.orders.append(ord2)
            db.session.add(ord2)
            db.session.add(client2)
            db.session.commit()
            ord3.products.append(prod2)
            client3.orders.append(ord3)
            db.session.add(ord3)
            db.session.add(client3)
            db.session.commit()
            return "Seeded successfully"

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('bp/page_not_found.html', type="new"), 404
    return app


#mysql://root:admin@localhost:3306/store
