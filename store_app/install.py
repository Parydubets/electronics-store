import os
import subprocess
import sys
from sqlalchemy_utils import database_exists, create_database

os.environ['FLASK_APP']='store'
db_user = os.environ['DB_USER']='root'		#mysql server username 
db_host = os.environ['DB_HOST']='127.0.0.1:3306'	#hostname:port
db_password = os.environ['DB_PASSWORD']='admin'	#mysql password
os.environ['FLASK_DEBUG']='1'		#debug mode: 0-off, 1-on


if db_password != '':
	db_user+=':'
database = 'mysql://{}{}@{}/store'.format(db_user,db_password,db_host)
if database_exists(database) == False:
	create_database(database)
	os.system("flask db upgrade")
	os.system("flask db migrate")
	os.system("flask db upgrade")
	os.system("flask seed")
os.system("flask run")			

