from sqlalchemy import Column, Integer, String, Text

from invoice_service.models.base import BaseModel


class ActiveItemFilter(BaseModel):
    __tablename__ = "active_item_filters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    field_name = Column(String(30), nullable=False)
    operation = Column(String(7), nullable=False)
    values = Column(Text, nullable=False)
