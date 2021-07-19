# acme

Application to facilitate product ingestion

### Installation
To install the project, first of all, create a virtualenv https://packaging.python.org/guides/installing-using-pip-and-virtualenv/ and then pip install requirements/base.txt

To install for development, create a virtualenv and then pip install -r requirements/dev.txt

Then run migrations python manage.py migrate while at the base folder for the project

Then run the server python manage.py runserver 8000

### Contributing
To contribute pick up one of the issues and then make a pull request.

### Raising Issues
If one finds an issue that needs to be fixed, they can raise an issue on https://github.com/lincmba/acme/issues

### Running Celery Worker
This project uses http://docs.celeryproject.org/en/latest/ to run asynchronous tasks such as sending emails. To run the celery worker:

$ cd root folder of the project

$ celery --app acme worker --loglevel=INFO