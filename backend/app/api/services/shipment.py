from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.shipment import ShipmentCreate
from app.database.models import Shipment, ShipmentStatus


class ShipmentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Shipment:
        shipment = await self.session.get(Shipment, id)
        if shipment is None:
            raise ValueError(f"Shipment with ID {id} not found.")
        return shipment
    
    async def add(self, shipment_create: ShipmentCreate) -> Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.PLACED,
            estimated_delivery=datetime.now() + timedelta(days=3)
        )

        self.session.add(new_shipment)
        await self.session.commit()
        await self.session.refresh(new_shipment)

        return new_shipment

    async def update(self, id: int, shipment_update: dict) -> Shipment:
        shipment = await self.get(id)
        shipment.sqlmodel_update(shipment_update)
        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)

        return shipment
    
    async def delete(self, id: int) -> None:
        await self.session.delete(
            await self.get(id)
        )
        
        await self.session.commit()
