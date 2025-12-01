from pydantic import BaseModel, Field
from typing import List
from .item import Item


class OptimizeRequest(BaseModel):
    budget: float = Field(..., gt=0, description="Orçamento disponível")
    items: List[Item] = Field(..., min_length=1, description="Lista de itens para otimizar")

    class Config:
        json_schema_extra = {
            "example": {
                "budget": 1000.00,
                "items": [
                    {"id": 1, "name": "Mouse", "price": 50.00, "priority": 5},
                    {"id": 2, "name": "Teclado", "price": 150.00, "priority": 8},
                    {"id": 3, "name": "Monitor", "price": 800.00, "priority": 9}
                ]
            }
        }
