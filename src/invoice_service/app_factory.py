from flask import Flask, g

from invoice_service.api.invoice_service_api import invoices
from invoice_service.api.line_item_api import line_items
from invoice_service.services import LINE_ITEM_SERVICE, INVOICE_SERVICE, FILTER_SERVICE
from invoice_service.services.invoice_service import InvoiceService
from invoice_service.services.item_filter_service import ItemFilterService
from invoice_service.services.line_item_service import LineItemService
from invoice_service.services.service_factory import ServiceFactory


def build_service_factory(app):
    service_factory = ServiceFactory(app)
    service_factory.register_service(LINE_ITEM_SERVICE, LineItemService)
    service_factory.register_service(INVOICE_SERVICE, InvoiceService)
    service_factory.register_service(FILTER_SERVICE, ItemFilterService)
    return service_factory


def create_app(config_file=None, config=None, service_factory_builder=build_service_factory) -> Flask:
    app = Flask(__name__)
    if config_file:
        app.config.from_pyfile(config_file)
    if config:
        app.config.update(config)
    app.register_blueprint(line_items)
    app.register_blueprint(invoices)
    _service_factory = service_factory_builder(app)

    class ContextGlobals(Flask.app_ctx_globals_class):
        service_factory = _service_factory

    app.app_ctx_globals_class = ContextGlobals
    return app
