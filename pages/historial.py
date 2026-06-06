import streamlit as st
import pandas as pd
from datetime import datetime
from db.queries import get_logs
from utils.units import from_kg


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

    df_v = df[["date", "exercise_name", "weight", "reps", "rir", "is_dropset", "notes"]].copy()
    df_v["date"] = df_v["date"].dt.strftime("%d/%m/%y")
    df_v["weight"] = df_v["weight"].apply(lambda w: from_kg(w, display_unit))
    df_v["is_dropset"] = df_v["is_dropset"].map({True: "🔴", False: ""})
    df_v["rir"] = df_v["rir"].apply(lambda x: f"{int(x)}" if pd.notna(x) else "")

    df_v.columns = ["Fecha", "Ejercicio", f"Peso ({display_unit})", "Reps", "RIR", "DS", "Notas"]

    st.caption(f"{len(df_v)} registros")
    st.dataframe(df_v, use_container_width=True, hide_index=True, height=420)

    st.download_button(
        "📥 Descargar CSV",
        data=df_v.to_csv(index=False),
        file_name=f"gym_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True,
    )
