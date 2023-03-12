# electronics-store

This is an electronics store application. 
Additional information and functionality will be added further.

# Electronics-store
## Epam final project


Build success by Travis-CI
[![Build Status](https://app.travis-ci.com/Parydubets/electronics-store.svg?branch=main)](https://app.travis-ci.com/Parydubets/electronics-store)
Coverage by coveralls
[![Coverage Status](https://coveralls.io/repos/github/Parydubets/electronics-store/badge.svg?branch=main)](https://coveralls.io/github/Parydubets/electronics-store?branch=main)

Electronics-store is flask app for electronics store managers. It allows to manipulate orders. clients and products 

## Features

- Manipulating clients both with interface and api (read, edit, delete)
- Manipulating orders both with interface and api (read, edit, delete)
- Manipulating products both with interface and api (read, edit, delete)
- Sorting each list of entities

Code coverage is available on coveralls.io
Code score by pylint is shown when building project with travis-ci (before coveralls line)
Builds are available on https://app.travis-ci.com/github/Parydubets/electronics-store

## Installation

This app uses additional software you should have:
- MySQL server


To run application on itself localy  you should clone it from repo with 

```sh
git clone https://github.com/Parydubets/electronics-store.git
```
Then set environment variables in electronics-store/store_app/install.py and run command:
```sh
python install.py
```
The script will create database if it doesn't exist and run the app
After run you can  access app at http://127.0.0.1:5000/


## Running with gunicorn
To run with gunicorn you need to have gunicorn installed in you local environment
Also you have to set such env variables:
 - FLASK_APP=store  
 - DB_USER=<user_of_active_mysql _server>
 - DB_HOST=<mysql_host_and_port_in_format_host:port>
 - DB_PASSWORD=<mysql_server_password> if there`s no password DB_PASSWORD=''

And run  following command: 
```sh
gunicorn -w <number_of_workers> 'store:create_app()'
```
In electronics-store/store_app folder
The project will be accesseble on http://127.0.0.1:8000/

## API

This project have a branch of api available:
- http://127.0.0.1:5000/api/clients_list <br>
 GET request: Returns list of clients <br>
 POST request: Creates new client on POST request
- http://127.0.0.1:5000/api/client/<id> <br>
 GET request: Returns client's information by client id <br>
 PUT request: Edits client by id <br>
 DELETE request: Deletes client by id


- http://127.0.0.1:5000/api/orders_list <br>
 GET request: Returns list of orders <br>
 POST request: Creates new order on POST request
- http://127.0.0.1:5000/api/order/<id> <br>
GET request: Returns order information by order id <br>
PUT request: Edits order by id <br>
DELETE request: Deletes order by id


- http://127.0.0.1:5000/api/products_list <br>
 GET request: Returns list of products <br>
 POST request: Creates new product on POST request
- http://127.0.0.1:5000/api/product/<id> <br>
 GET request: Returns product information by product id <br>
 PUT request: Edits product by id <br>
 DELETE request: Deletes product by id


- http://127.0.0.1:5000/api/orders_list/client/<id> <br>
 GET request: Returns list of orders by client`s id
- http://127.0.0.1:5000/api/orders/sum <br>
 GET request: Returns sum of all saved orders
- http://127.0.0.1:5000/api/client/<id>/sum <br>
 GET request: Returns sum of all orders by client id


## Attention
Tests for this application are written with pytest
For more deep testing everytime tests package is running, it recreates database
