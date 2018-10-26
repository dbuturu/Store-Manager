# Store-Manager

## Introduction

[![Build Status](https://travis-ci.org/dbuturu/Store-Manager.svg?branch=Develop)](https://travis-ci.org/dbuturu/Store-Manager)
[![Maintainability](https://api.codeclimate.com/v1/badges/aeea17bd89a8c2235747/maintainability)](https://codeclimate.com/github/dbuturu/Store-Manager/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/aeea17bd89a8c2235747/test_coverage)](https://codeclimate.com/github/dbuturu/Store-Manager/test_coverage)
[![Coverage Status](https://coveralls.io/repos/github/dbuturu/Store-Manager/badge.svg?branch=Develop)](https://coveralls.io/github/dbuturu/Store-Manager?branch=Develop)

### Installing

Clone this repository
git clone https://github.com/dbuturu/Store-Manager.git
Check out this branch.
git checkout Develop

#### Set up virtual environment

instal virtualenv using

    pip install virtualenv

Create a virtual environment using

    virtualenv venv

Active it by a run active command
for linux or mac

    source venv/bin/activate

or

    source venv/Scripts/activate

for windows

    venv\activate.bat

#### Storing environment variables 

set up an env file containg this
    FLASK_APP
    JWT_SECRET_KEY
    APP_CONFIG
    DATABASE_URL
    JWT_BLACKLIST_ENABLED

#### Running the application

Install dependencies by running
 `pip install -r requirements.txt`
Start the application by running
 `flask run`

#### Testing

Run Tests by running
    `pytest -v`

### API-Endpoints
 /products/
* get
  * read all products
* post
  * Add a product

 /products/{product_id}
* delete
  * delete specific product
* put
  * update specific product
* get
  * read specific product

 /sales/
* get
  * read all sales
* post
  * create a sale

 /sales/{sale_id}
* delete
  * delete specific sale
* put
  * update specific sale
* get
  * read all sales

 /users/
* get
  * read all users
* post
  * create a user

 /users/login/
* post
  * login a user

 /users/logout/
* post
  * logout a user

 /users/{username}
* delete
  * delete specific user
* put
  * update specific user
* get
  * read all users