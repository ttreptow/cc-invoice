class ItemNotFound(Exception):
    pass


class ReadOnlyItemValueError(Exception):
    pass


class InvoiceService:
    def get_line_items(self):
        return None

    def update_line_item(self, item_id, attributes):
        pass
