from flask import Flask

from invoice_service.api.line_item_api import line_items


def create_app() -> Flask:
    app = Flask(__name__)

    app.register_blueprint(line_items)
    return app
