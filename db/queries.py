import streamlit as st
from db.supabase_client import get_client

sb = get_client()

# ─── Rutinas ──────────────────────────────────────────────────────────────────

@st.cache_data(ttl=300)
def get_routines() -> list[dict]:
    return sb.table("routines").select("*").order("muscle_group").order("exercise_name").execute().data


def add_routine(exercise_name: str, muscle_group: str) -> None:
    sb.table("routines").insert({
        "exercise_name": exercise_name,
        "muscle_group": muscle_group,
    }).execute()


def update_routine_group(exercise_name: str, muscle_group: str) -> None:
    sb.table("routines").update({"muscle_group": muscle_group}).eq("exercise_name", exercise_name).execute()


def remove_routine(exercise_name: str) -> None:
    sb.table("routines").delete().eq("exercise_name", exercise_name).execute()


# ─── Logs ─────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=60)
def get_logs() -> list[dict]:
    return sb.table("workout_logs").select("*").order("date", desc=True).execute().data


def save_log(exercise_name, date, weight_input, unit, reps, rir, is_dropset, notes) -> None:
    from utils.units import to_kg, to_lb

    # Calcular ambas representaciones a partir del valor ingresado
    weight_kg = to_kg(weight_input, unit)
    weight_lb = to_lb(weight_input, unit)

    sb.table("workout_logs").insert({
        "exercise_name": exercise_name,
        "date":          date.isoformat(),
        "weight":        weight_kg,   # columna original, mantenerla por compatibilidad
        "weight_kg":     weight_kg,
        "weight_lb":     weight_lb,
        "unit":          unit,        # unidad con la que se ingresó
        "reps":          int(reps),
        "rir":           int(rir) if rir is not None else None,
        "is_dropset":    is_dropset,
        "notes":         notes or None,
    }).execute()


def delete_log(log_id: int) -> None:
    sb.table("workout_logs").delete().eq("id", log_id).execute()
