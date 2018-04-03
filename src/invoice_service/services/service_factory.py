from flask import g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.local import LocalProxy


class InvalidServiceError(Exception):
    pass


class ServiceFactory:
    @staticmethod
    def get_service_factory():
        return g.service_factory

    @classmethod
    def create_proxy_service(cls, service_name):
        def load_service():
            service_factory = cls.get_service_factory()
            return service_factory.get_service(service_name)

        return LocalProxy(load_service)

    def __init__(self, flask_app):
        self.db = SQLAlchemy(flask_app)
        self.registry = {}

    @property
    def session_maker(self):
        return self.db.session

    def register_service(self, service_name, service_builder):
        self.registry[service_name] = service_builder

    def get_service(self, service_name):
        if service_name not in self.registry:
            raise InvalidServiceError(service_name)
        if not hasattr(g, service_name):
            setattr(g, service_name, self.registry[service_name](self))
        return getattr(g, service_name)
