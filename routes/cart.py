from fastapi import APIRouter
from routes.budget import cart_state

router = APIRouter(tags=["Cart"])


@router.post("/reset")
async def reset_cart():
    cart_state.reset()
    return {
        "message": "Carrinho resetado com sucesso",
        "budget": cart_state.budget,
        "items": cart_state.items
    }


@router.get("/cart/status")
async def get_cart_status():
    total_price = sum(item['price'] for item in cart_state.items)
    total_priority = sum(item['priority'] for item in cart_state.items)
    
    return {
        "budget": cart_state.budget,
        "items_count": len(cart_state.items),
        "items": cart_state.items,
        "total_price": round(total_price, 2),
        "total_priority": total_priority,
        "remaining_if_all": round(cart_state.budget - total_price, 2) if cart_state.budget > 0 else None
    }
