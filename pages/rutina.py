import streamlit as st
from db.queries import get_routines, add_routine, update_routine_group, remove_routine

# Grupos predefinidos (el usuario puede escribir el suyo igual)
DEFAULT_GROUPS = ["Empuje", "Jale", "Piernas", "Hombros", "Brazos", "Cardio", "Sin grupo"]


def render() -> None:
    st.subheader("Mi rutina")
    st.caption("Ejercicios y grupos musculares")

    routines = get_routines()

    if not routines:
        st.info("Sin ejercicios todavía")
    else:
        # Agrupar por grupo muscular
        groups: dict[str, list[dict]] = {}
        for r in routines:
            g = r.get("muscle_group") or "Sin grupo"
            groups.setdefault(g, []).append(r)

        for group_name in sorted(groups.keys()):
            st.markdown(f'<div class="group-header">{group_name}</div>', unsafe_allow_html=True)
            for r in groups[group_name]:
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.markdown(f"**{r['exercise_name']}**")
                with col2:
                    new_group = st.selectbox(
                        "Grupo",
                        DEFAULT_GROUPS,
                        index=DEFAULT_GROUPS.index(r.get("muscle_group") or "Sin grupo")
                        if r.get("muscle_group") in DEFAULT_GROUPS else len(DEFAULT_GROUPS) - 1,
                        key=f"grp_{r['exercise_name']}",
                        label_visibility="collapsed",
                    )
                    if new_group != (r.get("muscle_group") or "Sin grupo"):
                        update_routine_group(r["exercise_name"], new_group)
                        st.cache_data.clear()
                        st.rerun()
                with col3:
                    if st.button("✕", key=f"del_{r['exercise_name']}"):
                        remove_routine(r["exercise_name"])
                        st.cache_data.clear()
                        st.rerun()

    st.divider()
    st.markdown("**Agregar ejercicio**")

    col1, col2 = st.columns(2)
    with col1:
        new_ex = st.text_input("Nombre", placeholder="Ej: Press de Banca")
    with col2:
        new_group_input = st.selectbox("Grupo muscular", DEFAULT_GROUPS, key="new_group")

    if st.button("Agregar a mi rutina", type="primary"):
        if new_ex.strip():
            try:
                add_routine(new_ex.strip(), new_group_input)
                st.cache_data.clear()
                st.success(f"✓ {new_ex} agregado en {new_group_input}")
                st.rerun()
            except Exception:
                st.error("Ya existe un ejercicio con ese nombre")
        else:
            st.error("Escribe el nombre del ejercicio")
