## Aproch

I used Django for the backend. First, I created models based on the fields present in the CSV file and set up a PostgreSQL database. Using the Django admin panel, I stored all the CSV data in the PostgreSQL database. Then, I used React for the frontend to display the data with different filters and search options. Only the first 10 rows are displayed on a page, and the user can navigate to the next or previous page.


## Tech Stack

## Backend (Django + PostgreSQL):

* Django 4.x

* Django REST Framework

* PostgreSQL

* django-filter

* Gunicorn

* Whitenoise

### Frontend (React):

* React 18.x

* Axios / Fetch API

* React Router

## Setup & Installation

##### retail_project -> Backend Folder

##### truestate-frontend -> Frontend Folder


### Clone the repository

```
git clone https://github.com/rishee10/TruEstate.git
cd TruEstate
```


### Backend (Django + PostgreSQL)

* Create The Virtual Enviroment for Backend

```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

* Install dependencies:

```
pip install -r requirements.txt
```

* Configure settings.py:

```
DEBUG = True
ALLOWED_HOSTS = []
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',  (My Database name is truestate_retail you need to create this database in pgadmin)
        'USER': 'your_db_user',  (My User name is postgres)
        'PASSWORD': 'your_db_password', 
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Apply migrations:

```
python manage.py makemigrations
```

```
python manage.py migrate
```

### Run Server

```
python manage.py runserver
```


### Frontend Setup (React)

#### Install dependencies:

```
cd truestate-frontend
```

```
npm install
```

### Build production-ready frontend:

```
npm run build
```

### Start the Server

```
npm start
```

You can view with this link: 









