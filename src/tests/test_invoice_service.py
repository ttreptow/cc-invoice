from invoice_service.models.line_item import LineItem
from invoice_service.operations.line_item_operations import grand_total

ITEMS = [
  {
    "id": 1,
    "campaign_id": 1,
    "campaign_name": "Satterfield-Turcotte : Multi-channelled next generation analyzer - e550",
    "line_item_name": "Awesome Plastic Car - 6475",
    "booked_amount": 430706.6871532752,
    "actual_amount": 401966.50504006835,
    "adjustments": 1311.0731142230268
  },
  {
    "id": 2,
    "campaign_id": 1,
    "campaign_name": "Satterfield-Turcotte : Multi-channelled next generation analyzer - e550",
    "line_item_name": "Fantastic Plastic Shirt - 278c",
    "booked_amount": 242951.09516407287,
    "actual_amount": 244249.26860341238,
    "adjustments": -2550.0901180359815
  }
]

CAMPAIGN_3_ITEMS = [
    {
        "id": 69,
        "campaign_id": 3,
        "campaign_name": "Rath-Yundt : Vision-oriented bottom-line knowledge base - 5126",
        "line_item_name": "Gorgeous Rubber Gloves - 0a2a",
        "booked_amount": 791534.9346784434,
        "actual_amount": 698914.4504033325,
        "adjustments": 47781.578823506105
    },
    {
        "id": 70,
        "campaign_id": 3,
        "campaign_name": "Rath-Yundt : Vision-oriented bottom-line knowledge base - 5126",
        "line_item_name": "Incredible Steel Table - bc45",
        "booked_amount": 282849.4341641974,
        "actual_amount": 258271.39897460229,
        "adjustments": 0.0
    }
]


class TestInvoiceService:
    def test_get_total_no_line_items(self, invoice_service):
        total = invoice_service.get_total()

        assert total == 0

    def test_get_total_with_items(self, invoice_service, line_item_service):
        line_items = [LineItem(**item) for item in ITEMS]
        expected_total = grand_total(line_items)
        line_item_service.add_items(line_items)

        total = invoice_service.get_total()

        assert expected_total == total

    def test_get_subtotals_by_campaign(self, invoice_service, line_item_service):
        campaign_1_items = [LineItem(**item) for item in ITEMS]
        campaign_3_items = [LineItem(**item) for item in CAMPAIGN_3_ITEMS]
        expected_total_1 = grand_total(campaign_1_items)
        expected_total_3 = grand_total(campaign_3_items)
        line_item_service.add_items(campaign_1_items)
        line_item_service.add_items(campaign_3_items)

        totals = invoice_service.get_grouped_totals(group_by="campaign_id")

        assert expected_total_1 == totals[1]
        assert expected_total_3 == totals[3]
