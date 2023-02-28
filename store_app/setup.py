""" This is a setup module """

from setuptools import setup, find_packages
import os

os.system("export FLASK_APP=store")

os.system("export FLASK_APP=store")

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
    ],
)
