from setuptools import setup, find_packages

setup(
    name='Store',
    version='1.0.0.0',
    author='Bohdan Parydubets',
    description='An educational flask project',
    long_description='An educational flask project with MySQL database. Created RESTful API and tests',
    url='https://github.com/Parydubets',
    python_requires='>=3.9, <4',
    packages=find_packages(include=['Store']),
    install_requires=[
        "Flask==2.2.3",
        "Jinja2==3.1.2",
        "Werkzeug==2.2.3",
    ],

)