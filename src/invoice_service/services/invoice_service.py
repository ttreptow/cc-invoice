

class InvoiceService:
    def __init__(self, service_factory):
        self.session_maker = service_factory.session_maker
        self.service_factory = service_factory

    def get_total(self):
        return 0
