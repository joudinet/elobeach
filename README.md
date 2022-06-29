# Elo Beach

A Django project to manage team ratings, based on Rémi Coulom's
[Whole-History Rating (WHR)](http://remi.coulom.free.fr/WHR/WHR.pdf) algorithm.

## Installation

Edit `elobeach/settings.py` file to:
- configure the access to the database;
- set a secret key (and keep it secret);
- set DEBUG variable to False if your are in production.

Run the followings commands to:
- install Python's whr module in your environment;
- create a super user for the admin access;
- create the DB tables
- run the server
```
source bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Usage

Go to the admin/ section, log in as the superuser and fill in results

Enjoy the team ratings on the home page. It is dependent on the results only.
