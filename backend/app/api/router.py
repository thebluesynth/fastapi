from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import ServiceDep
from app.api.schemas.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate
from app.database.models import Shipment

router = APIRouter(prefix="/shipment", tags=["Shipment"])

@router.get("/", response_model=ShipmentRead)
async def get_shipment(id: int, service: ServiceDep):
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with id {id} not found."
        )
    
    return shipment

@router.post("/")
async def submit_shipment(shipment: ShipmentCreate, service: ServiceDep) -> Shipment:
    return await service.add(shipment)

@router.patch("/", response_model=ShipmentRead)
async def patch_shipment(id: int, shipment_update: ShipmentUpdate, service: ServiceDep):
    update = shipment_update.model_dump(exclude_none=True)
    
    if not update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with id {id} not found."
        )
    
    return await service.update(id, update)

@router.delete("/")
async def delete_shipment(id: int, service: ServiceDep) -> dict[str, str]:
    await service.delete(id)
    
    return {"detail": f"Shipment with id {id} is deleted."}
