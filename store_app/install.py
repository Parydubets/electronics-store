import os
import subprocess
import sys
from sqlalchemy_utils import database_exists, create_database

os.environ['FLASK_APP']='store'
db_user = os.environ['DB_USER']='admin'		#mysql server username 
db_host = os.environ['DB_HOST']='127.0.0.1:3306'	#hostname:port
db_password = os.environ['DB_PASSWORD']='password'	#mysql password
os.environ['FLASK_DEBUG']='0'		#debug mode: 0-off, 1-on


print(db_user,db_password,db_host)
if db_password != '':
	db_user+=':'
database = 'mysql://{}{}@{}/store'.format(db_user,db_password,db_host)
if database_exists(database) == False:
	print('------------------false-----------------')
	create_database(database)
	os.system("flask db upgrade")
	os.system("flask db migrate")
	os.system("flask db upgrade")
	os.system("flask seed")
os.system("flask run")			

