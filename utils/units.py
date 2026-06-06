LB_TO_KG = 0.453592
KG_TO_LB = 2.20462

UNITS = ["kg", "lb"]


def to_kg(value: float, unit: str) -> float:
    """Convierte cualquier unidad a kg para guardar en BD."""
    if unit == "lb":
        return round(value * LB_TO_KG, 2)
    return round(value, 2)


def from_kg(value_kg: float, unit: str) -> float:
    """Convierte kg (almacenado en BD) a la unidad deseada para mostrar."""
    if unit == "lb":
        return round(value_kg * KG_TO_LB, 1)
    return round(value_kg, 2)


def format_weight(value_kg: float, unit: str) -> str:
    """Devuelve string formateado: '80 kg' o '176.4 lb'."""
    return f"{from_kg(value_kg, unit)} {unit}"
