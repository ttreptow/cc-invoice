from sqlalchemy import Column, Integer, DateTime

from invoice_service.models.base import BaseModel


class Invoice(BaseModel):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    invoice_date = Column(DateTime, nullable=False)
