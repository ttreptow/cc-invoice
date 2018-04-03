from flask import json


class TestInvoiceServiceApi:
    def test_get_subtotal(self, app_client, dummy_invoice_service):
        dummy_invoice_service.get_total.return_value = 1234.56

        r = app_client.get("/invoices/current/total")

        assert r.status_code == 200
        assert json.loads(r.data) == 1234.56
