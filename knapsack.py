from typing import List, Dict

def knapsack_optimize(items: List[Dict], budget: float) -> Dict:
    if not items or budget <= 0:
        return {
            "selected_items": [],
            "total_price": 0,
            "total_priority": 0,
            "remaining_budget": budget
        }
    
    budget_cents = int(budget * 100)
    items_with_cents = []
    
    for item in items:
        items_with_cents.append({
            **item,
            'price_cents': int(item['price'] * 100)
        })
    
    n = len(items_with_cents)
    dp = [[0 for _ in range(budget_cents + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        item = items_with_cents[i - 1]
        price_cents = item['price_cents']
        priority = item['priority']
        
        for w in range(budget_cents + 1):
            dp[i][w] = dp[i - 1][w]
            
            if price_cents <= w:
                dp[i][w] = max(
                    dp[i][w],
                    dp[i - 1][w - price_cents] + priority
                )
    
    selected_items = []
    w = budget_cents
    
    for i in range(n, 0, -1):
        if w > 0 and dp[i][w] != dp[i - 1][w]:
            item = items_with_cents[i - 1]
            selected_item = {k: v for k, v in item.items() if k != 'price_cents'}
            selected_items.append(selected_item)
            w -= item['price_cents']
    
    selected_items.reverse()
    
    total_price = sum(item['price'] for item in selected_items)
    total_priority = sum(item['priority'] for item in selected_items)
    remaining_budget = budget - total_price
    
    return {
        "selected_items": selected_items,
        "total_price": round(total_price, 2),
        "total_priority": total_priority,
        "remaining_budget": round(remaining_budget, 2)
    }


def knapsack_optimize_detailed(items: List[Dict], budget: float) -> Dict:
    result = knapsack_optimize(items, budget)
    
    result['algorithm_info'] = {
        'name': 'Knapsack Problem (0/1)',
        'technique': 'Dynamic Programming',
        'time_complexity': f'O(n * W) onde n={len(items)} e W={int(budget * 100)}',
        'space_complexity': f'O(n * W)'
    }
    
    return result
