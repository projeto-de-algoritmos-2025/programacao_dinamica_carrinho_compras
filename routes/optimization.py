from fastapi import APIRouter, HTTPException
from models import OptimizeRequest
from routes.budget import cart_state
from knapsack import knapsack_optimize, knapsack_optimize_detailed

router = APIRouter(prefix="/optimize", tags=["Optimization"])


@router.post("")
async def optimize_cart(request: OptimizeRequest):
    items_list = [item.model_dump() for item in request.items]
    result = knapsack_optimize(items_list, request.budget)
    
    return {
        "message": "Otimização realizada com sucesso",
        **result
    }


@router.post("/current")
async def optimize_current_cart():
    if cart_state.budget <= 0:
        raise HTTPException(
            status_code=400,
            detail="Orçamento não foi definido. Use POST /budget primeiro."
        )
    
    if not cart_state.items:
        raise HTTPException(
            status_code=400,
            detail="Nenhum item no carrinho. Adicione itens usando POST /items."
        )
    
    result = knapsack_optimize(cart_state.items, cart_state.budget)
    
    return {
        "message": "Otimização realizada com sucesso",
        "budget_used": cart_state.budget,
        "items_analyzed": len(cart_state.items),
        **result
    }


@router.post("/detailed")
async def optimize_cart_detailed(request: OptimizeRequest):
    items_list = [item.model_dump() for item in request.items]
    result = knapsack_optimize_detailed(items_list, request.budget)
    
    return {
        "message": "Otimização detalhada realizada com sucesso",
        **result
    }
