from pydantic import BaseModel, Field
from typing import Optional


class Item(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1, description="Nome do item")
    price: float = Field(..., gt=0, description="Preço do item em reais")
    priority: int = Field(..., ge=1, le=10, description="Prioridade do item (1-10)")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Notebook",
                "price": 2999.90,
                "priority": 9
            }
        }
