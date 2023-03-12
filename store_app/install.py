import os
import subprocess
import sys

os.environ['DB_USER']='admin'		#mysql server username 
os.environ['DB_HOST']='127.0.0.1:3306'	#hostname:port
os.environ['DB_passwrod']='password'	#mysql password
os.environ['FLASK_DEBUG']='0'		#debug mode: 0-off, 1-on
os.system("flask db upgrade")
os.system("flask db migrate")
os.system("flask db upgrade")
os.system("flask seed")
os.system("flask run")			
