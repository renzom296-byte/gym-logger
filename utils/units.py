LB_TO_KG = 0.453592
KG_TO_LB = 2.20462

UNITS = ["kg", "lb"]


def to_kg(value: float, unit: str) -> float:
    """Convierte valor ingresado a kg."""
    if unit == "lb":
        return round(value * LB_TO_KG, 2)
    return round(value, 2)


def to_lb(value: float, unit: str) -> float:
    """Convierte valor ingresado a lb."""
    if unit == "kg":
        return round(value * KG_TO_LB, 2)
    return round(value, 2)


def pick_weight(row: dict, display_unit: str) -> float:
    """Elige la columna correcta de la BD según la unidad de display."""
    if display_unit == "lb":
        return row.get("weight_lb") or round((row.get("weight_kg") or row.get("weight", 0)) * KG_TO_LB, 2)
    return row.get("weight_kg") or row.get("weight", 0)


def format_weight(row: dict, display_unit: str) -> str:
    return f"{pick_weight(row, display_unit)} {display_unit}"
