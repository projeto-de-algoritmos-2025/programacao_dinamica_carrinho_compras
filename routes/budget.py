from fastapi import APIRouter
from models import BudgetRequest, CartState

router = APIRouter(prefix="/budget", tags=["Budget"])
cart_state = CartState()


@router.post("")
async def set_budget(request: BudgetRequest):
    cart_state.budget = request.budget
    return {
        "message": "Orçamento definido com sucesso",
        "budget": cart_state.budget
    }


@router.get("")
async def get_budget():
    return {"budget": cart_state.budget}
