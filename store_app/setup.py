""" This is a setup module """

from setuptools import setup, find_packages
import os

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
        "Flask==2.2.0",
        "Jinja2==3.0",
        "Werkzeug==2.2.3",
        "pylint==2.16.2",
        "pytest==7.2.1",
    ],
)
