from fastapi import APIRouter, HTTPException
from models import Item
from routes.budget import cart_state

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("")
async def add_item(item: Item):
    item_dict = item.model_dump()
    item_dict['id'] = cart_state.next_id
    cart_state.next_id += 1
    cart_state.items.append(item_dict)
    
    return {
        "message": "Item adicionado com sucesso",
        "item": item_dict
    }


@router.get("")
async def get_items():
    return {
        "items": cart_state.items,
        "count": len(cart_state.items)
    }


@router.get("/{item_id}")
async def get_item(item_id: int):
    item = next((item for item in cart_state.items if item['id'] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return item


@router.put("/{item_id}")
async def update_item(item_id: int, item: Item):
    index = next((i for i, item in enumerate(cart_state.items) if item['id'] == item_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    
    item_dict = item.model_dump()
    item_dict['id'] = item_id
    cart_state.items[index] = item_dict
    
    return {
        "message": "Item atualizado com sucesso",
        "item": item_dict
    }


@router.delete("/{item_id}")
async def delete_item(item_id: int):
    initial_length = len(cart_state.items)
    cart_state.items = [item for item in cart_state.items if item['id'] != item_id]
    
    if len(cart_state.items) == initial_length:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    
    return {
        "message": "Item deletado com sucesso",
        "id": item_id
    }


@router.delete("")
async def delete_all_items():
    count = len(cart_state.items)
    cart_state.items = []
    cart_state.next_id = 1
    
    return {
        "message": "Todos os itens foram deletados",
        "deleted_count": count
    }
