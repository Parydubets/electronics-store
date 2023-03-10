""" This is a setup module """

from setuptools import setup, find_packages
import os


os.system("flask db upgrade")
os.system("flask db migrate")
os.system("flask db upgrade")
os.system("flask seed")

setup(
    name='store',
    version='1.0.0.0',
    author='Bohdan Parydubets',
    description='An educational flask project',
    long_description='An educational flask project with'
                     ' MySQL database. Created RESTful API and tests',
    url='https://github.com/Parydubets',
    python_requires='>=3.9, <4',
    packages=find_packages(),
    install_requires=[
        "Flask==2.2.3",
        "Jinja2==3.0",
        "Werkzeug==2.2.3",
        "pylint==2.16.2",
        "pytest==7.2.1",
        "coveralls==3.3.1",
        "SQLAlchemy==2.0.4",
        "mysql==0.0.3",
        "mysqlclient==2.1.1",
        "Flask-SQLAlchemy==3.0.3",
        "Flask-Migrate==4.0.4",
        "click==8.1.3",
        "marshmallow==3.19.0",
        "marshmallow-sqlalchemy==0.29.0",
        "flask-marshmallow==0.14.0",
        "WTForms==3.0.1",
        "Flask-WTF==1.1.1",
        "email-validator==1.3.1",
        "SQLAlchemy-Utils==0.40.0",
        "flask_restful",
        "pylint",
        "grep",
    ],
)
