from datetime import datetime

from sqlalchemy.orm import scoped_session

from invoice_service.models.invoice import Invoice
from invoice_service.operations.line_item_operations import grand_total
from invoice_service.services import LINE_ITEM_SERVICE, FILTER_SERVICE
from invoice_service.services.item_filter_service import ItemFilterService
from invoice_service.services.line_item_service import LineItemService


class InvoiceService:
    def __init__(self, service_factory):
        self.session_maker = service_factory.session_maker
        self.line_item_service = service_factory.create_proxy_service(LINE_ITEM_SERVICE)  # type: LineItemService
        self.filter_service = service_factory.create_proxy_service(FILTER_SERVICE)  # type: ItemFilterService

    def get_total(self):
        return grand_total(self.line_item_service.get_line_items())

    def get_grouped_totals(self, group_by=None):
        items = self.line_item_service.get_grouped_items(group_by)
        return {group_id: grand_total(group_items) for group_id, group_items in items.items()}

    def finalize(self):
        invoice = Invoice(invoice_date=datetime.utcnow())
        session = self.session_maker()
        session.add(invoice)
        session.commit()
        invoice_id = invoice.id
        self.line_item_service.set_invoice(invoice_id)
        self.filter_service.clear_active_filters()
        return {"invoice_id": invoice_id}

