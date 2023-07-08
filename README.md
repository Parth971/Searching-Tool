
# Scraping Website

Scraping website is to search through huge amount of data. The data is scraped from 44 websites mentioned below. 



### 44 Websites

1. [Advanced Procurement for Universities and Colleges (APUC)](http://www.apuc-scot.ac.uk/)
2. [Crescent Purchasing Consortium (CPC)](https://www.thecpc.ac.uk/)
3. [Crown Commercial Service (CCS)](https://www.crowncommercial.gov.uk/)
4. [Dep of Finance](https://www.finance-ni.gov.uk/topics/procurement)
5. [East of England NHS Collaborative Procurement Hub](https://www.eoecph.nhs.uk/)
6. [Eastern Procurement](https://eastern-procurement.co.uk/)
7. [EN:Procure Ltd](https://www.efficiencynorth.org/procure)
8. [ESPO, formally the Eastern Shires Purchasing Organisation,](https://www.espo.org/)
9. [Fusion21 Members Consortium](https://www.fusion21.co.uk/)
10. [Grand Union Housing Group](https://www.guhg.co.uk/)
11. [Hampshire County Council](https://www.hants.gov.uk/business/procurement)
12. [HSC Business Services Organisation](https://hscbusiness.hscni.net/)
13. [KCS,](https://www.kcs.co.uk/)
14. [London Uni's Purchasing Consortium](https://www.lupc.ac.uk/)
15. [National Procurement Service](https://gov.wales/national-procurement-service)
16. [NEPO, the North East Purchasing Organisation,](https://www.nepo.org/)
17. [NEUPC, the North Eastern Universities Purchasing Consortium](https://neupc.ac.uk/ )
18. [NHS London Procurement Partnership](https://www.lpp.nhs.uk/ )
19. [NHS National Services Scotland](https://www.nss.nhs.scot/)
20. [NHS North of England Commercial Procurement Collaborative (NOE CPC, based in Sheffield)](https://www.noecpc.nhs.uk/)
21. [NHS Shared Business Services (NHS SBS)](https://www.sbs.nhs.uk/ )
22. [NHS Supply Chain](https://www.supplychain.nhs.uk/ )
23. [NHS Wales SPS](https://nwssp.nhs.wales/ )
24. [North and Mid Wales Trunk Road Agent](https://traffic.wales/north-and-mid-wales-trunk-road-agent-nmwtra )
25. [NWUPC, the North Western Universities Purchasing Consortium](https://www.nwupc.ac.uk/ )
26. [Pagabo](https://www.pagabo.co.uk/ )
27. [Places for People](https://www.placesforpeople.co.uk/ )
28. [Procure Partnerships](https://procurepartnerships.co.uk/ )
29. [Procurement Hub](https://www.procurementhub.co.uk/ )
30. [Scape](https://www.scape.co.uk/ )
31. [Public Contracts Scotland](https://www.publiccontractsscotland.gov.uk/Search/Search_MainPage.aspx)
32. [Scotland Excel](https://www.scotland-excel.org.uk/ )
33. [SUPC, the Southern Universities Purchasing Consortium](https://www.supc.ac.uk/ )
34. [TEC, the Energy Consortium](https://www.tec.ac.uk/ )
35. [The Higher Education Purchasing Consortium, (HEPCW)](http://www.hepcw.ac.uk/ )
36. [The Northern Ireland Government's Construction and Procurement Delivery (CPD) Collaborative Procurement Team](https://www.finance-ni.gov.uk/construction-procurement-delivery)
37. [TUCO, The University Caterers Organisation](https://www.tuco.ac.uk/ )
38. [WECA, the West of England Combined Authority](https://www.westofengland-ca.gov.uk/)
39. [YPO Yorkshire Purchasing Organisation](https://www.ypo.co.uk/ )
40. [Contracts Finder](https://www.gov.uk/contracts-finder )
41. [London Construction Parntership ](https://londonconstructionprogramme.co.uk/)
42. [Health Trust Europe](https://www.healthtrusteurope.com/ )
### Project desciption

First the data is scrapped from these 44 websites and stored in SQl database (postgres). Scrapper related code is present in `/scrapers` folder.
Now, for searching through this saved data, we use a website with `ReactJS-DRF` as our stack. For searching in such huge amount of data, we use `elasticsearch`.
Website related code is located at `/web`.

## Project Setup

Python Version: 3.10.6

Assumption: Project is cloned, and current working directory in terminal/cmd is `/web`.


### Set Python Virtual Environment (recommended)

Install [Python Virtual Environment](https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/)

To Activate virtual environment

For Linux

    source myenv/bin/activate 

For Windows

    myenv\Scripts\activate


### Install Required Python Packages

    pip install -r requirements.txt

### Create Environment

Create `.env` file

    # For Linux
    cp sample_env.txt .env

    # For Windows
    copy sample_env.txt .env

Change environment variables in `.env` file

#### Variables Description

- `SETTINGS_MODULE_NAME`: `dev`
- `ACCESS_TOKEN_LIFETIME`: `3600` # This value represent amount of time(in sec) to expire after creation of access_token
- `REFRESH_TOKEN_LIFETIME`: `86400` # This value represent amount of time(in sec) to expire after creation of refresh_token
- `FRONT_END_DOMAIN`: `http://localhost:3000` # This variable is used for creating links in send_email functionality
- `BACK_END_DOMAIN`: `http://localhost:8000` # This variable is used for creating links in send_email functionality
- `PASSWORD_RESET_TIMEOUT`: `60` # This value represents amount of time(in sec) to expire after creation, Using PasswordResetTokenGenerator (Used in Forgotpassword Api)
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

Run below commands to create tables in database

    python manage.py makemigrations
    python manage.py migrate

### Run elasticsearch
    
    # To do

### Run Server

To run Local Development Server, run below cmd

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

Run below command
    
    python manage.py deletedocuments 32929 92828 58593

