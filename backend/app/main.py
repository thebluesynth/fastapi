from typing import Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference  # type: ignore

from app.db import Database
from app.schemas import ShipmentRead, ShipmentCreate, ShipmentUpdate

app = FastAPI()
db = Database()

@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int):
    shipment = db.get_shipment(id)
    
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with id {id} not found."
        )
    
    return shipment

@app.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate) -> dict[str, int]:
    new_id = db.insert_shipment(shipment)

    return {"id": new_id}

@app.patch("/shipment", response_model=ShipmentRead)
def patch_shipment(id: int, shipment: ShipmentUpdate):
    updated_shipment = db.update_shipment(id, shipment)
    
    return updated_shipment

@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    db.delete_shipment(id)

    return {"detail": f"Shipment with id {id} is deleted."}

@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url = app.openapi_url,
        title = "Scalar API",
        )
