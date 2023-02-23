import os
from flask import Flask, Blueprint


app = Flask(__name__, instance_relative_config=True)
app.config['DEBUG']=True
app.config.from_mapping(
    SECRET_KEY='somerandomkey',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)
"""store = Blueprint('store', __name__,
                        template_folder='templates')
app.register_blueprint(store)"""

from Store import views

