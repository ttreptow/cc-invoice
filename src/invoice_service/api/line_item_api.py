from flask import Blueprint, abort, json, request

from invoice_service.api.serializer import serialize
from invoice_service.exceptions import ItemNotFound, ReadOnlyItemValueError, InvalidUpdateError
from invoice_service.services import LINE_ITEM_SERVICE, FILTER_SERVICE
from invoice_service.services.service_factory import ServiceFactory

line_items = Blueprint('line_items', __name__, url_prefix="/lineitems")


line_item_service = ServiceFactory.create_proxy_service(LINE_ITEM_SERVICE)
filter_service = ServiceFactory.create_proxy_service(FILTER_SERVICE)


@line_items.route("")
def get_line_items():
    return serialize(line_item_service.get_line_items())


@line_items.route("/filters", methods=['PUT', 'POST', 'DELETE'])
def set_filter():
    if request.method != "POST":
        filter_service.clear_active_filters()
    if request.method != "DELETE":
        filter_service.add_filter(**json.loads(request.data))
    return serialize("OK")


@line_items.route("/filters", methods=["GET"])
def get_active_filters():
    return serialize(filter_service.get_active_filters())


@line_items.route("/<item_id>", methods=['PUT'])
def update_line_item(item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        abort(404)
    try:
        return serialize(line_item_service.update_line_item(item_id, json.loads(request.data)))
    except ItemNotFound:
        abort(404)
    except ReadOnlyItemValueError:
        abort(401)
    except InvalidUpdateError:
        abort(400)
