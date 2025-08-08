from contextlib import asynccontextmanager
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference  # type: ignore

from app.database.models import Shipment, ShipmentStatus
from app.database.session import SessionDep, create_db_and_tables
from app.schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan_handler)

@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int, session: SessionDep):
    
    shipment = session.get(Shipment, id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with id {id} not found."
        )
    
    return shipment

@app.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate, session: SessionDep) -> dict[str, int]:
    new_shipment = Shipment(
        **shipment.model_dump(),
        status=ShipmentStatus.PLACED,
        estimated_delivery=datetime.now() + timedelta(days=3)
    )

    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)

    return {"id": new_shipment.id}

@app.patch("/shipment", response_model=ShipmentRead)
def patch_shipment(id: int, shipment_update: ShipmentUpdate, session: SessionDep):
    
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update."
        )
    
    shipment = session.get(Shipment, id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with id {id} not found."
        )
    shipment.sqlmodel_update(update)
    
    session.add(shipment)
    session.commit()
    session.refresh(shipment)

    return shipment

@app.delete("/shipment")
def delete_shipment(id: int, session: SessionDep) -> dict[str, str]:
    session.delete(
        session.get(Shipment, id)
    )
    session.commit()

    return {"detail": f"Shipment with id {id} is deleted."}

@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url = app.openapi_url,
        title = "Scalar API",
    )
