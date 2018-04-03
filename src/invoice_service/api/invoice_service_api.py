from flask import Blueprint, jsonify

from invoice_service.services import INVOICE_SERVICE
from invoice_service.services.service_factory import ServiceFactory

invoices = Blueprint('invoices', __name__, url_prefix="/invoices")


invoice_service = ServiceFactory.create_proxy_service(INVOICE_SERVICE)


@invoices.route("/current/total")
def get_invoice_total():
    return jsonify(invoice_service.get_total())


@invoices.route("/current/subtotals")
def get_subtotals():
    return jsonify(invoice_service.get_grouped_totals(group_by="campaign_id"))
