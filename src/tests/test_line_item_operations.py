from invoice_service.models.line_item import LineItem
from invoice_service.operations.line_item_operations import billable_amount, grand_total


def test_billable_amount():
    item = LineItem(actual_amount=123.4, adjustments=456.7)

    billable = billable_amount(item)

    assert 580.1 == billable


def test_grand_total():
    items = [LineItem(actual_amount=50, adjustments=50), LineItem(actual_amount=100, adjustments=500)]

    assert 700 == grand_total(items)
