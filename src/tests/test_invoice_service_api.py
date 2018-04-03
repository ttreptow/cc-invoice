from flask import json


class TestInvoiceServiceApi:
    def test_get_total(self, app_client, dummy_invoice_service):
        dummy_invoice_service.get_total.return_value = 1234.56

        r = app_client.get("/invoices/current/total")

        assert r.status_code == 200
        assert json.loads(r.data) == 1234.56

    def test_get_subtotal(self, app_client, dummy_invoice_service):
        grouped_subtotals = {1: 1234.5, 2: 5678.9}
        dummy_invoice_service.get_grouped_totals.return_value = grouped_subtotals

        r = app_client.get("/invoices/current/subtotals")

        assert r.status_code == 200
        # json always converts dict keys to strings
        assert json.loads(r.data) == json.loads(json.dumps(grouped_subtotals))
        dummy_invoice_service.get_grouped_totals.assert_called_once_with(group_by="campaign_id")
