from flask import json


class TestInvoiceServiceApi:
    def test_get_total(self, app_client, dummy_invoice_service):
        dummy_invoice_service.get_total.return_value = 1234.56

        r = app_client.get("/invoices/current/total")

        assert 200 == r.status_code
        assert 1234.56 == json.loads(r.data)

    def test_get_subtotal(self, app_client, dummy_invoice_service):
        grouped_subtotals = {1: 1234.5, 2: 5678.9}
        dummy_invoice_service.get_grouped_totals.return_value = grouped_subtotals

        r = app_client.get("/invoices/current/subtotals")

        assert 200 == r.status_code
        # json always converts dict keys to strings
        assert json.loads(json.dumps(grouped_subtotals)) == json.loads(r.data)
        dummy_invoice_service.get_grouped_totals.assert_called_once_with(group_by="campaign_id")

    def test_finalize_invoice(self, app_client, dummy_invoice_service):
        dummy_invoice_service.finalize.return_value = "something"
        r = app_client.post("/invoices/finalized")

        assert 201 == r.status_code
        assert "something" == json.loads(r.data)
