def validate_ingredients(ingredients: str) -> str:
    from .light_spellbook import light_spell_allowed_ingredients

    lowered = ingredients.lower()
    allowed = light_spell_allowed_ingredients()
    status = "INVALID"
    if any(ingredient in lowered for ingredient in allowed):
        status = "VALID"
    return f"{ingredients} - {status}"
