[![Patrick Luboobi](https://img.shields.io/badge/Patrick%20Luboobi-BucketListAPI-green.svg)]()
[![Build Status](https://travis-ci.org/patlub/BucketListAPI.svg?branch=dev)](https://travis-ci.org/patlub/BucketListAPI)
[![Coverage Status](https://coveralls.io/repos/github/patlub/BucketListAPI/badge.svg?branch=dev)](https://coveralls.io/github/patlub/BucketListAPI?branch=dev)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)]()
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

# BucketList API

A Bucket list is a list of items a person wishes to accomplish.
This API is used to Perform CRUD operations on the BucketList

>The API is hosted live on heroku; 

>https://patrickluboobi-bucket-list-api.herokuapp.com/

# Project description

Brief highlights about the following concepts is necessary:

 >API

 >REST

 >JSON

**API**

An **API**, acronym for Application Programming Interface, provides a blueprint for how software programs interacts with each other.

**REST**

REST is an acronym that stands for **RE**presentational **S**tate **T**ransfer and has become the de-facto way of building API's and thus API's using this standard are known as RESTFul API's. The five main principles the implementation of REST and RESTFulness are:

>Everything is a resource.

>Every resource has a unique identifier.

>Use simple and uniform interfaces.

>Communication is done by representation.

>Aim to be Stateless.

**JSON**

Yet another acronym, JSON which stands for **J**avascript **O**bject **N**otation, is a light-weight format that facilitates interchange of data between different systems or, case in point, software. It is intended to be universal and thus allows consumption of data by any program regardless of the programming language it is written in. Sample JSON data would be as follows:

```
{
    "name":"John Does",
    "email":"johndoe@gmail.com",
}

```

## Installation
 
Clone the GitHub repo:
 
http:
>`$ git clone https://github.com/patlub/BucketListAPI.git`

cd into the folder and install a [virtual environment](https://virtualenv.pypa.io/en/stable/)

`$ virtualenv venv`

Activate the virtual environment

`$ venv/bin/activate`

Install all app requirements

`$ pip install -r requirements.txt`
Create the database and run migrations

`$ createdb bucketlist_db`

`$ createdb testing_db`

`$ python manage.py db init`

`$ python manage.py db migrate`

`$ python manage.py db upgrade`

All done! Now, start your server by running `python manage.py runserver`. You could use a GUI platform like [postman](https://www.getpostman.com/) to make requests to and fro the api.
### Endpoints

Here is a list of all the endpoints in bucketlist app.

Endpoint | Functionality| Access
------------ | ------------- | ------------- 
POST /auth/register | Registers a user | PUBLIC
POST /auth/login |Logs a user in | PUBLIC
POST /buckets/ | Creates a new bucket list | PRIVATE
GET /buckets/ | Lists all created bucket lists | PRIVATE
GET /buckets/id | Gets a single bucket list with the suppled id | PRIVATE
PUT /buckets/id | Updates bucket list with the suppled id | PRIVATE
DELETE /buckets/id | Deletes bucket list with the suppled id | PRIVATE
POST /buckets/id/items/ | Creates a new item in bucket list | PRIVATE
PUT /buckets/id/items/item_id | Updates a bucket list item | PRIVATE
DELETE /buckets/id/items/item_id | Deletes an item in a bucket list | PRIVATE

### Testing
The application tests are based on python’s unit testing framework unittest.
To run tests with nose, run:
 
 `nosetests`

And you should see 
>All 37 tests Passed
