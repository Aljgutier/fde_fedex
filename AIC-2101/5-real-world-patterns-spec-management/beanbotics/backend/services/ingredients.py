"""
Ingredient Service

Loads ingredient cost data and customization mappings from JSON.
"""

import json
from pathlib import Path
from typing import Dict


class IngredientService:
    def __init__(self):
        self.ingredients: Dict[str, dict] = {}
        self.customization_mappings: Dict[str, Dict[str, float]] = {}
        self._load_ingredients()

    def _load_ingredients(self):
        data_file = Path(__file__).parent.parent / "data" / "ingredients.json"
        with open(data_file, "r") as f:
            data = json.load(f)

        for entry in data["ingredients"]:
            for field in ("id", "name", "unit", "cost_per_unit"):
                if field not in entry:
                    raise ValueError(f"Ingredient missing required field '{field}': {entry}")
            if entry["cost_per_unit"] < 0:
                raise ValueError(f"Ingredient has negative cost: {entry}")
            self.ingredients[entry["id"]] = entry

        self.customization_mappings = data.get("customization_mappings", {})

    def get_ingredient_cost(self, ingredient_id: str) -> float:
        return self.ingredients[ingredient_id]["cost_per_unit"]

    def calculate_recipe_cost(self, recipe: Dict[str, float]) -> float:
        total = 0.0
        for ingredient_id, quantity in recipe.items():
            unit_cost = self.ingredients[ingredient_id]["cost_per_unit"]
            total += unit_cost * quantity
        return round(total, 2)

    def calculate_customization_cost(self, customization_ids: list) -> float:
        total = 0.0
        for cid in customization_ids:
            mapping = self.customization_mappings.get(cid, {})
            for ingredient_id, quantity in mapping.items():
                unit_cost = self.ingredients[ingredient_id]["cost_per_unit"]
                total += unit_cost * quantity
        return round(total, 2)
