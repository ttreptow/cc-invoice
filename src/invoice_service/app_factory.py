from flask import Flask, g

from invoice_service.service import InvoiceService


def create_app() -> Flask:
    app = Flask(__name__)
    return app


def get_service():
    if not hasattr(g, "invoice_service"):
        set_service()
    return g.invoice_service


def set_service(service=None):
    g.invoice_service = service or InvoiceService()
