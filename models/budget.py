from pydantic import BaseModel, Field


class BudgetRequest(BaseModel):
    budget: float = Field(..., gt=0, description="Orçamento disponível em reais")

    class Config:
        json_schema_extra = {
            "example": {
                "budget": 5000.00
            }
        }
