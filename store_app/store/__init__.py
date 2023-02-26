""" The app initialization file """
import os
from flask import Flask, Blueprint


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='somerandomkey',
            DATABASE=os.path.join(app.instance_path, 'store.sqlite'),
    )
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

    import store.views
    app.register_blueprint(store.views.bp)
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    return app

