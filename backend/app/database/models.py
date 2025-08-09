from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class ShipmentStatus(str, Enum):
    PLACED = "Placed"
    In_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    OUT_FOR_DELIVERY = "Out for Delivery"

class Shipment(SQLModel, table=True):
    __tablename__ = "shipment"

    id: int = Field(primary_key=True)
    content: str
    weight: float = Field(ge=1, lt=25)
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime
