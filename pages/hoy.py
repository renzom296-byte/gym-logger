import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from db.queries import get_logs
from utils.units import format_weight


def render(display_unit: str) -> None:
    logs = get_logs()

    if not logs:
        st.info("Sin registros. Empieza en 📝")
        return

    df = pd.DataFrame(logs)
    df["date"] = pd.to_datetime(df["date"])
    hoy = datetime.now().date()
    df_hoy = df[df["date"].dt.date == hoy]

    st.markdown(f"**{hoy.strftime('%A %d de %B').capitalize()}**")

    if df_hoy.empty:
        st.info("Sin registros de hoy todavía")
    else:
        for _, row in df_hoy.iterrows():
            badges = ""
            if row.get("is_dropset"):
                badges += '<span class="badge-ds">DROPSET</span> '
            if pd.notna(row.get("rir")):
                badges += f'<span class="badge-rir">RIR {int(row["rir"])}</span>'
            note_html = f"<div class='note'>{row['notes']}</div>" if row.get("notes") else ""

            st.markdown(f"""
            <div class="log-card">
                <div class="exname">{row['exercise_name']}</div>
                <div class="detail">{format_weight(row, display_unit)} × {int(row['reps'])} reps &nbsp;{badges}</div>
                {note_html}
            </div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("**Últimos 7 días**")
    df_semana = df[df["date"].dt.date >= hoy - timedelta(days=7)]

    if df_semana.empty:
        st.caption("Sin actividad esta semana")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Días activos", df_semana["date"].dt.date.nunique())
        with col2:
            st.metric("Sets registrados", len(df_semana))
