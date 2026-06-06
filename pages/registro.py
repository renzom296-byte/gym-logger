import streamlit as st
from datetime import datetime
from db.queries import get_routines, save_log, get_logs
from utils.units import UNITS, format_weight


def render(display_unit: str) -> None:
    routines = get_routines()

    if not routines:
        st.warning("Ve a ⚙️ Rutina y agrega tus ejercicios primero")
        return

    # Agrupar por grupo muscular
    groups: dict[str, list[str]] = {}
    for r in routines:
        g = r.get("muscle_group") or "Sin grupo"
        groups.setdefault(g, []).append(r["exercise_name"])

    selected_group = st.selectbox("Grupo muscular", sorted(groups.keys()),
                                  label_visibility="collapsed", key="reg_group")
    selected_exercise = st.selectbox("Ejercicio", groups[selected_group],
                                     label_visibility="collapsed", key="reg_exercise")
    fecha = st.date_input("Fecha", value=datetime.now().date())

    # Último registro de este ejercicio
    logs = get_logs()
    prev = next((l for l in logs if l["exercise_name"] == selected_exercise), None)
    if prev:
        st.caption(f"Último: **{format_weight(prev, display_unit)} × {prev['reps']} reps**")

    st.divider()
    st.markdown("**Carga y volumen**")

    # Inicializar reg_unit desde display_unit si no existe
    if "reg_unit" not in st.session_state:
        st.session_state.reg_unit = display_unit

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        input_unit = st.selectbox("Unidad", UNITS, key="reg_unit")
    with col2:
        step = 0.5 if input_unit == "kg" else 1.0
        weight_input = st.number_input(f"Peso ({input_unit})", min_value=0.0, step=step, value=0.0)
    with col3:
        reps = st.number_input("Reps", min_value=1, step=1, value=10)

    # Preview de la conversión siempre visible
    from utils.units import to_kg, to_lb
    if input_unit == "kg":
        st.caption(f"≡ {to_lb(weight_input, 'kg')} lb")
    else:
        st.caption(f"≡ {to_kg(weight_input, 'lb')} kg")

    st.divider()
    st.markdown("**Esfuerzo**")

    use_rir = st.checkbox("Registrar RIR")
    rir = None
    if use_rir:
        rir = st.select_slider(
            "RIR",
            options=[0, 1, 2, 3, 4, 5],
            value=2,
            format_func=lambda x: {
                0: "0 — Fallo 💀",
                1: "1 — Casi fallo 🥵",
                2: "2 — Difícil 🔥",
                3: "3 — Moderado 💪",
                4: "4 — Cómodo 😐",
                5: "5 — Fácil 😊",
            }[x],
        )

    is_dropset = st.checkbox("🔴 Incluí dropset")
    notes = st.text_area("Notas", placeholder="Cómo te sentiste, qué pasó...",
                         height=80, label_visibility="collapsed")

    st.divider()

    if st.button("Guardar registro", type="primary"):
        if weight_input > 0:
            save_log(selected_exercise, fecha, weight_input, input_unit, reps, rir, is_dropset, notes)
            st.cache_data.clear()
            st.success(f"✓ {selected_exercise}: {weight_input} {input_unit} × {reps} reps guardado")
            st.rerun()
        else:
            st.error("El peso debe ser mayor a 0")
