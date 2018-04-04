# cc-invoice
This is an application I wrote for a coding challenge. It is a simple Flask app with RESTful(ish) APIs backed by SQLAlchemy.

## Installation
1. Install Python 3.6 or newer and ensure the bin directory is on the path (the directory is called "Scripts" on Windows)
1. Change to the src directory and run 
```pip install .```
1. Change back to the root directory (where this readme is)
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

## Available APIs
### GET /lineitems
Gets the active (not part of a finalized invoice) line items, filtered by any filters set with the filters API
### PUT /lineitems/\<id\>
Updates a line item

Payload should be a JSON dictionary with the format:
```json
{
"adjustments": 1234.5
}
```

### PUT /lineitems/filter
Sets a filter on the line items

Payload:
```json
{
"field_name": "name of line item field to filter", # , e.g. "campaign_id"
"operation": "eq", #one of "eq" or "in"
"values": # for "eq", a single value, for "in" a list of values
}
```

### GET /invoices/current/total
Gets the total for the current filtered line items

### GET /invoices/current/subtotals
Gets the subtotals grouped by campaign id for filtered line items

### PUT /invoices/finalized
Finalizes the invoice with the current filtered line items.


## Running tests
1. Install pytest with ```pip install pytest```
1. Run tests with ```pytest``` (it should find the tests automatically)
