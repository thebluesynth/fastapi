from fastapi import APIRouter, HTTPException, status

from app.api.schemas.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate
from app.api.services.shipment import ShipmentService
from app.database.models import Shipment
from app.database.session import SessionDep

router = APIRouter(prefix="/shipment", tags=["Shipment"])

@router.get("/", response_model=ShipmentRead)
async def get_shipment(id: int, session: SessionDep):
    shipment = await ShipmentService(session).get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with id {id} not found."
        )
    
    return shipment

@router.post("/")
async def submit_shipment(shipment: ShipmentCreate, session: SessionDep) -> Shipment:
    return await ShipmentService(session).add(shipment)

@router.patch("/", response_model=ShipmentRead)
async def patch_shipment(id: int, shipment_update: ShipmentUpdate, session: SessionDep):
    
    update = shipment_update.model_dump(exclude_none=True)
    
    if not update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with id {id} not found."
        )
    
    return await ShipmentService(session).update(id, update)

@router.delete("/")
async def delete_shipment(id: int, session: SessionDep) -> dict[str, str]:
    await ShipmentService(session).delete(id)
    
    return {"detail": f"Shipment with id {id} is deleted."}
