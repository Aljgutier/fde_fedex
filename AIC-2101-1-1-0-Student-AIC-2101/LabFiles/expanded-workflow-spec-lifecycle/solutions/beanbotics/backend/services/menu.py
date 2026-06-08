"""
Menu Service

Loads and serves the BeanBotics drink menu from JSON data.
"""

import json
from pathlib import Path
from typing import List, Optional, Set

from backend.models import MenuItem


class MenuService:
    def __init__(self):
        self.items: List[MenuItem] = []
        self._load_menu()

    def _load_menu(self):
        data_file = Path(__file__).parent.parent / "data" / "menu.json"
        with open(data_file, "r") as f:
            menu_data = json.load(f)
        self.items = [MenuItem(**item) for item in menu_data]

    def validate_recipes(self, valid_ingredient_ids: Set[str]):
        for item in self.items:
            for size_name, size_info in item.sizes.items():
                if "recipe" not in size_info:
                    raise ValueError(
                        f"Menu item '{item.id}' size '{size_name}' is missing a recipe"
                    )
                recipe = size_info["recipe"]
                for ingredient_id, quantity in recipe.items():
                    if ingredient_id not in valid_ingredient_ids:
                        raise ValueError(
                            f"Recipe for '{item.id}' size '{size_name}' references "
                            f"unknown ingredient '{ingredient_id}'"
                        )
                    if quantity <= 0:
                        raise ValueError(
                            f"Recipe for '{item.id}' size '{size_name}' has non-positive "
                            f"quantity {quantity} for ingredient '{ingredient_id}'"
                        )

    def get_all_items(self) -> List[MenuItem]:
        return self.items

    def get_item_by_id(self, item_id: str) -> Optional[MenuItem]:
        for item in self.items:
            if item.id == item_id:
                return item
        return None
