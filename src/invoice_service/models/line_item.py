from sqlalchemy import Column, Integer, Float, String, ForeignKey

from invoice_service.models.base import BaseModel


class LineItem(BaseModel):
    __tablename__ = "line_items"

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, nullable=False)
    campaign_name = Column(String(150), nullable=False)
    line_item_name = Column(String(100), nullable=False)
    booked_amount = Column(Float, nullable=False)
    actual_amount = Column(Float, nullable=False)
    adjustments = Column(Float, nullable=False)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=True)
