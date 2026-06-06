import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from db.queries import get_logs, get_routines
from utils.units import from_kg, format_weight


def render(display_unit: str) -> None:
    logs = get_logs()

    if not logs:
        st.info("Sin datos todavía")
        return

    df = pd.DataFrame(logs)
    df["date"] = pd.to_datetime(df["date"])

    # Agrupar ejercicios por grupo muscular para el selector
    routines = get_routines()
    group_map = {r["exercise_name"]: r.get("muscle_group") or "Sin grupo" for r in routines}

    ejercicios = sorted(df["exercise_name"].unique())

    # Selector agrupado por grupo muscular
    groups: dict[str, list[str]] = {}
    for ex in ejercicios:
        g = group_map.get(ex, "Sin grupo")
        groups.setdefault(g, []).append(ex)

    group_sel = st.selectbox("Grupo", sorted(groups.keys()), label_visibility="collapsed", key="prog_group")
    ejercicio_sel = st.selectbox("Ejercicio", groups[group_sel], label_visibility="collapsed", key="prog_ex")

    df_ej = df[df["exercise_name"] == ejercicio_sel].sort_values("date").reset_index(drop=True)

    if df_ej.empty:
        st.info("Sin registros para este ejercicio")
        return

    last = df_ej.iloc[-1]
    first = df_ej.iloc[0]

    diff_w = from_kg(last["weight"], display_unit) - from_kg(first["weight"], display_unit)
    diff_r = int(last["reps"]) - int(first["reps"])

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Peso actual", format_weight(last["weight"], display_unit), f"{diff_w:+.1f} {display_unit}")
    with col2:
        st.metric("Reps actuales", int(last["reps"]), f"{diff_r:+d}")

    st.divider()

    # Convertir pesos para display
    df_ej["weight_display"] = df_ej["weight"].apply(lambda w: from_kg(w, display_unit))

    # Gráfico peso
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_ej["date"], y=df_ej["weight_display"],
        mode="lines+markers",
        line=dict(color="#1a1a1a", width=2),
        marker=dict(size=7, color="#1a1a1a"),
        hovertemplate=f"%{{y}} {display_unit}<extra></extra>"
    ))
    fig.update_layout(
        title=f"Peso ({display_unit})", height=230,
        margin=dict(l=0, r=0, t=32, b=0),
        xaxis=dict(showgrid=False, tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0", tickfont=dict(size=10)),
        plot_bgcolor="white", paper_bgcolor="white"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Gráfico reps
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=df_ej["date"], y=df_ej["reps"],
        mode="lines+markers",
        line=dict(color="#999", width=2),
        marker=dict(size=7, color="#999"),
    ))
    fig2.update_layout(
        title="Reps", height=230,
        margin=dict(l=0, r=0, t=32, b=0),
        xaxis=dict(showgrid=False, tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0", tickfont=dict(size=10)),
        plot_bgcolor="white", paper_bgcolor="white"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.subheader("⏱️ Tiempo en cada carga")

    periodos = []
    f_inicio = df_ej.iloc[0]["date"]
    p_ref = df_ej.iloc[0]["weight"]
    r_ref = int(df_ej.iloc[0]["reps"])

    for i, row in df_ej.iterrows():
        if row["weight"] != p_ref or int(row["reps"]) != r_ref:
            dias = (row["date"] - f_inicio).days
            periodos.append({
                "Carga": f"{from_kg(p_ref, display_unit)} {display_unit} × {r_ref}",
                "Desde": f_inicio.strftime("%d/%m/%y"),
                "Días": dias,
            })
            p_ref = row["weight"]
            r_ref = int(row["reps"])
            f_inicio = row["date"]

    dias_actual = (df_ej.iloc[-1]["date"] - f_inicio).days
    periodos.append({
        "Carga": f"{from_kg(p_ref, display_unit)} {display_unit} × {r_ref}",
        "Desde": f_inicio.strftime("%d/%m/%y"),
        "Días": dias_actual,
    })

    st.dataframe(pd.DataFrame(periodos), use_container_width=True, hide_index=True)
    st.info(f"Llevas **{dias_actual} días** con **{from_kg(p_ref, display_unit)} {display_unit} × {r_ref} reps**")
