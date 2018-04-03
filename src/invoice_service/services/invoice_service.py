from invoice_service.operations.line_item_operations import grand_total
from invoice_service.services import LINE_ITEM_SERVICE
from invoice_service.services.line_item_service import LineItemService


class InvoiceService:
    def __init__(self, service_factory):
        self.session_maker = service_factory.session_maker
        self.line_item_service = service_factory.create_proxy_service(LINE_ITEM_SERVICE)  # type: LineItemService

    def get_total(self):
        return grand_total(self.line_item_service.get_line_items())

    def get_grouped_totals(self, group_by=None, values=None):
        items = self.line_item_service.get_grouped_items(group_by, values)
        return {group_id: grand_total(group_items) for group_id, group_items in items.items()}
