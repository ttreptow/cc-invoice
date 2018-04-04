# cc-invoice
This is an application I wrote for a coding challenge. It is a simple Flask app with RESTful APIs backed by SQLAlchemy.

## Installation
1. Install Python 3.6 or newer and ensure the bin directory is on the path (the directory is called "Scripts" on Windows)
1. Change to the src directory and run 
```pip install .```
1. Run the app.

Linux:
```
export FLASK_APP=src/invoice_service/app.py
export CCINVOICE_CONFIG=ccinvoice.cfg
flask run
```

Windows: 
```
set FLASK_APP=src\invoice_service\app.py
set CCINVOICE_CONFIG=ccinvoice.cfg
flask run
```

## Running tests
1. Install pytest with ```pip install pytest```
1. Run tests with ```pytest``` (it should find the tests automatically)
