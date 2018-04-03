from flask import g

from invoice_service.services.line_item_service import InvoiceService


def get_service():
    if not hasattr(g, "invoice_service"):
        set_service()
    return g.invoice_service


def set_service(service=None):
    g.invoice_service = service or InvoiceService()
