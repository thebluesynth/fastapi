from datetime import datetime

from pydantic import BaseModel, Field

from app.database.models import ShipmentStatus


class BaseShipment(BaseModel):
    content: str = Field(max_length=30, description="Content of the shipment")
    weight: float = Field(ge=1, lt=25, description="Weight must be between 1 and 25 kg")
    destination: int = Field(description="Destination ZIP code")

class ShipmentRead(BaseShipment):
    status: ShipmentStatus
    estimated_delivery: datetime

class ShipmentCreate(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)
    