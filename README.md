# cowin-notify
CoWin Vaccination Slot Availablity Email Notification Using Python

Get an email notification if there is a vaccination slot available at your location, by running this script on your computer.

NB: There is no guarantee if CoWin blocks API

## Use Cases
* Able to get slots by District - (Pass only district_id or pincode at a time). 
* Able to get slots by Pincode - (Pass only district_id or pincode at a time).
* Filter by age (45 or 18) - By default is 45 (optional).
* Filter by date ("DD/MM/YYYY")- By default date is taken as Tomorrow (optional).

## Starting app

    $ python app.py


## Setup of development environment

First install required dependencies.

If you have already used poetry(https://pypi.org/project/poetry/)
Use Poetry for dependency and environment.

After that, create your virtualenv:

    $ virtualenv -p python3.8 env3
    
Activate virtualenv:

    $ source <path>/env3/bin/activate

Install Requirements:

    $ pip install -r requirements.txt
    
    
Create `.env` file in root folder.

Copy env variables from `.sample-env` and use your own data.

`DISTRICT_ID` is available at `datasets/districts.json`.
        
And to start the app:

    $ python app.py
    
## Version
* Python : 3.8+
