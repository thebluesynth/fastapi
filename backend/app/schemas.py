from enum import Enum
from pydantic import BaseModel, Field

class ShipmentStatus(str, Enum):
    PLACED = "Placed"
    In_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    OUT_FOR_DELIVERY = "Out for Delivery"

class BaseShipment(BaseModel):
    content: str = Field(max_length=30, description="Content of the shipment")
    weight: float = Field(ge=1, lt=25, description="Weight must be between 1 and 25 kg")
    destination: int = Field(description="Destination ZIP code")

class ShipmentRead(BaseShipment):
    status: ShipmentStatus

class ShipmentCreate(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
