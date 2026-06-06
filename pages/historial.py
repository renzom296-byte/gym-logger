import streamlit as st
import pandas as pd
from datetime import datetime
from db.queries import get_logs
from utils.units import pick_weight


def render(display_unit: str) -> None:
    logs = get_logs()
    if not logs:
        st.info("Sin historial")
        return

    df = pd.DataFrame(logs)
    df["date"] = pd.to_datetime(df["date"])

    filtro = st.selectbox(
        "Filtrar por ejercicio",
        ["Todos"] + sorted(df["exercise_name"].unique().tolist()),
        label_visibility="collapsed",
    )
    if filtro != "Todos":
        df = df[df["exercise_name"] == filtro]

    df_v = df.copy()
    df_v["date"]       = df_v["date"].dt.strftime("%d/%m/%y")
    df_v["peso"]       = df_v.apply(lambda r: pick_weight(r, display_unit), axis=1)
    df_v["unidad"]     = df_v["unit"].fillna("kg")   # unidad con la que se ingresó
    df_v["is_dropset"] = df_v["is_dropset"].map({True: "🔴", False: ""})
    df_v["rir"]        = df_v["rir"].apply(lambda x: str(int(x)) if pd.notna(x) else "")

    df_v = df_v[["date", "exercise_name", "peso", "unidad", "reps", "rir", "is_dropset", "notes"]]
    df_v.columns = ["Fecha", "Ejercicio", f"Peso ({display_unit})", "Ingresado", "Reps", "RIR", "DS", "Notas"]

    st.caption(f"{len(df_v)} registros  ·  mostrando en {display_unit}")
    st.dataframe(df_v, use_container_width=True, hide_index=True, height=420)

    st.download_button(
        "📥 Descargar CSV",
        data=df_v.to_csv(index=False),
        file_name=f"gym_{datetime.now().strftime('%Y%m%d')}_{display_unit}.csv",
        mime="text/csv",
        use_container_width=True,
    )
