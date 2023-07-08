
# Searching Tool

Searching Tool is a DRF-based project to search through huge amounts of data. The data is scraped from websites. 


### Project description

First, the data is scrapped from multiple websites and stored in an SQL database (Postgres).
Now, To search through such a huge amount of data, we used `elasticsearch`.


## Project Setup

Python Version: 3.10.6

Assumption: The project is cloned, and the current working directory in terminal/cmd is `/Searching-Tool`.


### Set Python Virtual Environment (recommended)

Install [Python Virtual Environment](https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/)

To Activate the virtual environment

For Linux

    source myenv/bin/activate 

For Windows

    myenv\Scripts\activate


### Install Required Python Packages

    pip install -r requirements.txt

### Create Environment

Create a `.env` file

    # For Linux
    cp sample_env.txt .env

    # For Windows
    copy sample_env.txt .env

Change environment variables in the `.env` file

#### Variables Description

- `SETTINGS_MODULE_NAME`: `dev`
- `ACCESS_TOKEN_LIFETIME`: `3600` # This value represent amount of time(in sec) to expire after creation of access_token
- `REFRESH_TOKEN_LIFETIME`: `86400` # This value represent amount of time(in sec) to expire after creation of refresh_token
- `FRONT_END_DOMAIN`: `http://localhost:3000` # This variable is used for creating links in send_email functionality
- `BACK_END_DOMAIN`: `http://localhost:8000` # This variable is used for creating links in send_email functionality
- `PASSWORD_RESET_TIMEOUT`: `60` # This value represents the amount of time(in seconds) to expire after creation, Using PasswordResetTokenGenerator (Used in Forgotpassword Api)
- `INQUIRY_EMAIL`: `sending@fake.com` # This email will receive inquiry emails
- `DB_NAME`: `database_name`
- `DB_USER`: `database_user_name`
- `DB_PASS`: `database_user_password`
- `DB_PORT`: `database_port`
- `DB_HOST`: `database_host`
- `EMAIL_HOST_USER`: `email address` # This email is used in send_email functionality to send mails to users
- `EMAIL_HOST_PASSWORD`: `app password` # This is app password created from Google account
- `ELASTICSEARCH_USERNAME`: `elastic` # This is username of elasticsearch server
- `ELASTICSEARCH_PASSWORD`: `password` # This is password of elasticsearch server
- `ELASTICSEARCH_HOST_IP`: `localhost` # This is host ip of elasticsearch server
- `ELASTICSEARCH_HOST_PORT`: `9200` # This is host port of elasticsearch server
- `FRAMEWORK_INDEX_NAME`: `framework_test` # This is index name of framework in elasticsearch


### Database Migrations

Run the below commands to create tables in the database

    python manage.py makemigrations
    python manage.py migrate


### Run elasticsearch
    
    Follow steps in [Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/run-elasticsearch-locally.html)


### Run Server

To run Local Development Server, run the below cmd

    python manage.py runserver

To run using GUNICORN

    gunicorn core.wsgi:application --bind 0.0.0.0:8000 --timeout 600 --daemon


## Populate Database

### Populate Survey Related Data

Run below command

    python manage.py survey_init

### Populate Framework Values (Used in "Search by values" drop-down)

Run below command

    python manage.py framework_values

### Populate Fake Scraped Data

Run below command

    python manage.py populate_frameworks

### Index Database Data to Elasticsearch

Run below command
    
    # Delete index and rebuild
    python manage.py search_index --rebuild
    
    # Create index if not and update
    python manage.py search_index --populate

### Delete Document from Elasticsearch by Id

Run the below command
    
    python manage.py deletedocuments 32929 92828 58593

