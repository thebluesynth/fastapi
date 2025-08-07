import sqlite3
from typing import Any

from .schemas import ShipmentCreate, ShipmentUpdate

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("shipments.db", check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS shipments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                weight REAL NOT NULL,
                destination TEXT NOT NULL,
                status TEXT NOT NULL
            )
        ''')
        self.connection.commit()
    
    def insert_shipment(self, shipment: ShipmentCreate) -> int:
        self.cursor.execute("SELECT MAX(id) FROM shipments")
        result = self.cursor.fetchone()
        id = result[0] + 1 if result[0] is not None else 1
        self.cursor.execute('''
            INSERT INTO shipments 
            VALUES (:id, :content, :weight, :destination, :status)
        ''',
            {
                "id": id, 
                 **shipment.model_dump(),
                "status": "Placed"
            }
        )
        self.connection.commit()

        return id

    def get_shipment(self, id: int) -> dict[str, Any] | None:
        self.cursor.execute('''
            SELECT * FROM shipments
            WHERE id = ?
        ''', (id,))
        row = self.cursor.fetchone()
        
        return {
            "id": row[0],
            "content": row[1],
            "weight": row[2],
            "destination": row[3],
            "status": row[4]
        } if row else None
    
    def update_shipment(self, id: int, shipment: ShipmentUpdate) -> dict[str, Any]:
        self.cursor.execute('''
            UPDATE shipments SET status = :status
            WHERE id = :id
        ''',
            {
                "id": id,
                **shipment.model_dump()
            }
        )
        self.connection.commit()

        if self.get_shipment(id) is None:
            raise ValueError(f"Shipment with id {id} not found.")
        
        updated_shipment = self.get_shipment(id)
        if updated_shipment is None:
            raise ValueError(f"Shipment with id {id} does not exist.")
        
        return updated_shipment


    def delete_shipment(self, id: int) -> None:
        self.cursor.execute('''
            DELETE FROM shipments
            WHERE id = ?
        ''', (id,))
        self.connection.commit()
    
    def close(self):
        self.connection.close()