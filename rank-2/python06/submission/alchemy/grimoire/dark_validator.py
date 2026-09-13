from .dark_spellbook import dark_spell_allowed_ingredients


def validate_ingredients(ingredients: str) -> str:
    lowered = ingredients.lower()
    allowed = dark_spell_allowed_ingredients()
    status = "INVALID"
    if any(ingredient in lowered for ingredient in allowed):
        status = "VALID"
    return f"{ingredients} - {status}"
