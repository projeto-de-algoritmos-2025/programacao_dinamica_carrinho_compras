from typing import List


class CartState:
    def __init__(self):
        self.budget: float = 0
        self.items: List[dict] = []
        self.next_id: int = 1

    def reset(self):
        self.budget = 0
        self.items = []
        self.next_id = 1
