![open issues](https://img.shields.io/github/issues/Praveen2105/NSAC-Trailblazers)
![open issues](https://img.shields.io/github/forks/Praveen2105/NSAC-Trailblazers)
![open issues](https://img.shields.io/github/stars/Praveen2105/NSAC-Trailblazers)
![open issues](https://img.shields.io/github/contributors/Praveen2105/NSAC-Trailblazers)
[![Visits Badge](https://badges.pufler.dev/visits/Praveen2105/NSAC-Trailblazers)](https://badges.pufler.dev)

# Spot-That-Fire-V3.0-Nasa-Space-Apps-Challenge
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/uses-html.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/uses-css.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/uses-js.svg)](https://forthebadge.com)

## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Usage](#usage)
* [Screenshots](#screenshots)

[Deployed](https://forestfires.co/html/index-2.html)

## About the Project
Our project leverages pioneering AI techniques to detect wildfire at very early stages, way faster than the current systems used.
The system seamlessly detects fire with data from various sources like IoT devices, satellite data and data provided by users living nearby the forest. The use of different technologies gives us unique advantage and helps detect wildfire faster. Our system also provides great features like smart routing, smart alert system, emergency centre finder, and much more to the users in case a wildfire occurs.


## Getting Started
### Prerequisites

* HTML CSS JS
* Python
* Django


### Installation

* Installing GeoDjango Dependencies (GEOS, GDAL, and PROJ.4)
    
    ```
    $ sudo aptitude install gdal-bin libgdal-dev
    $ sudo aptitude install python3-gdal
  
    $ sudo aptitude install binutils libproj-dev
    ```
    
    

* Backend
    
    * To Setup Celery and Redis
    
    ```
    $ pip install Celery
    $ pip install redis
    $ brew install redis
    $ pip install -r requirements.txt
    ```
    
    * Setting up a Spatial Database With PostgreSQL and PostGIS
        
        ```Python
        $ sudo apt-get update
        $ sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib
        $ sudo su - postgres
        $ psql
        ```
        * Create Database, User and Grant all permissions
        
        ```Python
        postgres=# CREATE DATABASE trailblazers;
        postgres=# CREATE USER sanyam WITH PASSWORD 'sanyam';
        postgres=# CREATE USER sanyam WITH PASSWORD 'sanyam';
        postgres=# ALTER ROLE sanyam SET client_encoding TO 'utf8';
        postgres=# ALTER ROLE sanyam SET default_transaction_isolation TO 'read committed';
        postgres=# ALTER ROLE sanyam SET timezone TO 'UTC';   
        ```
    * OR Using docker
    
    ```Python
    $ docker run --name=postgis -d -e POSTGRES_USER=sanyam -e POSTGRES_PASS=sanyam -e POSTGRES_DBNAME=trailblazers -p 5432:5432 kartoza/postgis:9.6-2.4
    ```
    
    * Migrations
    
    ```Python
    $ python manage.py makemigrations
    $ python manage.py migrate
    ```

### Usage

* To Create Super User

    ```
    $ python manage.py createsuperuser
    ```
  
* To Runserver

    ``` python
    $ brew services start redis
    $ celery -A backend2 worker -l info
    ```
  
    ``` python
    $ python manage.py runserver
    ```
 
## Screenshots
<img src = "https://github.com/Praveen2105/NSAC-Trailblazers/blob/main/Screenshots/whatwedo.JPG" height = "500" width = "800">
<img src = "https://github.com/Praveen2105/NSAC-Trailblazers/blob/main/Screenshots/3.png" height = "500" width = "800">
<img src = "https://github.com/Praveen2105/NSAC-Trailblazers/blob/main/Screenshots/1.png" height = "500" width = "800">
