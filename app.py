import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
from supabase import create_client, Client

st.set_page_config(
    page_title="Gym Logger",
    page_icon="💪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── CSS Mobile-First ─────────────────────────────────────────────────────────
st.markdown("""
<style>
#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 1rem 1rem 5rem 1rem !important;
    max-width: 480px !important;
    margin: auto;
}

/* Tabs grandes para dedo */
.stTabs [data-baseweb="tab-list"] { gap: 0; border-bottom: 1px solid #e0e0e0; }
.stTabs [data-baseweb="tab"] {
    padding: 14px 0 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    flex: 1;
    text-align: center;
    letter-spacing: 0.3px;
}
.stTabs [aria-selected="true"] {
    border-bottom: 2px solid #1a1a1a !important;
    color: #1a1a1a !important;
}

/* Inputs grandes */
input[type="number"], input[type="text"], textarea {
    font-size: 16px !important;
    min-height: 48px !important;
    border-radius: 10px !important;
}

/* Boton primario */
.stButton > button[kind="primary"] {
    width: 100%;
    height: 52px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    border-radius: 14px !important;
    background-color: #1a1a1a !important;
    color: white !important;
    border: none !important;
    margin-top: 8px;
}

/* Selectbox */
.stSelectbox > div > div {
    min-height: 48px !important;
    border-radius: 10px !important;
    font-size: 16px !important;
}

/* Number input centrado */
.stNumberInput > label { font-size: 13px !important; font-weight: 500; color: #888; }
.stNumberInput > div > div > div > input {
    font-size: 22px !important;
    font-weight: 700 !important;
    text-align: center !important;
    min-height: 56px !important;
    border-radius: 10px !important;
}

/* Metricas */
[data-testid="metric-container"] {
    background: #f8f8f8;
    border-radius: 14px;
    padding: 14px 16px !important;
}
[data-testid="metric-container"] > label {
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #888 !important;
}
[data-testid="metric-container"] > div {
    font-size: 24px !important;
    font-weight: 700 !important;
    color: #1a1a1a !important;
}

h1 { font-size: 22px !important; font-weight: 700 !important; margin-bottom: 0 !important; }
h3 { font-size: 16px !important; font-weight: 600 !important; }
hr { margin: 1rem 0 !important; border-color: #f0f0f0 !important; }

.badge-ds { display:inline-block; background:#fff0f0; color:#c0392b; font-size:10px; font-weight:700; padding:2px 7px; border-radius:20px; }
.badge-rir { display:inline-block; background:#f0f4ff; color:#2c5282; font-size:10px; font-weight:700; padding:2px 7px; border-radius:20px; }

.log-card {
    background: white;
    border: 1px solid #f0f0f0;
    border-radius: 14px;
    padding: 14px 16px;
    margin-bottom: 10px;
}
.log-card .exname { font-size: 15px; font-weight: 700; color: #1a1a1a; }
.log-card .detail { font-size: 13px; color: #888; margin-top: 4px; }
.log-card .note { font-size: 12px; color: #aaa; margin-top: 6px; font-style: italic; }
</style>
""", unsafe_allow_html=True)

# ─── Supabase ─────────────────────────────────────────────────────────────────
@st.cache_resource
def init_supabase():
    return create_client(st.secrets["supabase_url"], st.secrets["supabase_key"])

try:
    supabase: Client = init_supabase()
except:
    st.error("Error de conexion. Revisa tus credenciales en Secrets.")
    st.stop()

@st.cache_data(ttl=300)
def get_routines():
    return supabase.table("routines").select("*").order("exercise_name").execute().data

@st.cache_data(ttl=60)
def get_logs():
    return supabase.table("workout_logs").select("*").order("date", desc=True).execute().data

def save_log(exercise_name, date, weight, reps, rir, is_dropset, notes):
    supabase.table("workout_logs").insert({
        "exercise_name": exercise_name,
        "date": date.isoformat(),
        "weight": float(weight),
        "reps": int(reps),
        "rir": int(rir) if rir is not None else None,
        "is_dropset": is_dropset,
        "notes": notes or None
    }).execute()

def add_routine(name):
    supabase.table("routines").insert({"exercise_name": name}).execute()

def remove_routine(name):
    supabase.table("routines").delete().eq("exercise_name", name).execute()

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("# 💪 Gym Logger")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Registrar", "🕐 Hoy", "📈 Progreso", "📋 Historial", "⚙️ Rutina"])

# ══════════════════════════════════════════
# TAB 1 — REGISTRAR
# ══════════════════════════════════════════
with tab1:
    routines = get_routines()
    exercises = [r["exercise_name"] for r in routines]

    if not exercises:
        st.warning("Ve a ⚙️ Rutina y agrega tus ejercicios primero")
    else:
        selected = st.selectbox("Ejercicio", exercises, label_visibility="collapsed")
        fecha = st.date_input("Fecha", value=datetime.now().date())
        st.divider()

        st.markdown("**Carga y volumen**")
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Peso (kg)", min_value=0.0, step=0.5, value=0.0)
        with col2:
            reps = st.number_input("Reps", min_value=1, step=1, value=10)

        st.divider()
        st.markdown("**Extras**")

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
                    5: "5 — Fácil 😊"
                }[x]
            )

        is_dropset = st.checkbox("🔴 Incluí dropset")
        notes = st.text_area("Notas", placeholder="Cómo te sentiste, qué pasó...", height=80, label_visibility="collapsed")

        st.divider()
        if st.button("Guardar registro", type="primary"):
            if weight > 0:
                save_log(selected, fecha, weight, reps, rir, is_dropset, notes)
                st.cache_data.clear()
                st.success(f"✓ {selected}: {weight}kg × {reps} reps guardado")
                st.rerun()
            else:
                st.error("El peso debe ser mayor a 0")


# ══════════════════════════════════════════
# TAB 2 — HOY
# ══════════════════════════════════════════
with tab2:
    logs = get_logs()
    if not logs:
        st.info("Sin registros. Empieza en 📝")
    else:
        df = pd.DataFrame(logs)
        df['date'] = pd.to_datetime(df['date'])
        hoy = datetime.now().date()
        df_hoy = df[df['date'].dt.date == hoy]

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
                note_html = f"<div class='note'>{row['notes']}</div>" if row.get('notes') else ""
                st.markdown(f"""
                <div class="log-card">
                    <div class="exname">{row['exercise_name']}</div>
                    <div class="detail">{row['weight']} kg × {int(row['reps'])} reps &nbsp; {badges}</div>
                    {note_html}
                </div>""", unsafe_allow_html=True)

        st.divider()
        st.markdown("**Últimos 7 días**")
        df_semana = df[df['date'].dt.date >= hoy - timedelta(days=7)]
        if df_semana.empty:
            st.caption("Sin actividad esta semana")
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Días activos", df_semana['date'].dt.date.nunique())
            with col2:
                st.metric("Sets registrados", len(df_semana))


# ══════════════════════════════════════════
# TAB 3 — PROGRESO
# ══════════════════════════════════════════
with tab3:
    logs = get_logs()
    if not logs:
        st.info("Sin datos todavía")
    else:
        df = pd.DataFrame(logs)
        df['date'] = pd.to_datetime(df['date'])
        ejercicio_sel = st.selectbox("Ver progreso de", sorted(df['exercise_name'].unique()), label_visibility="collapsed")
        df_ej = df[df['exercise_name'] == ejercicio_sel].sort_values('date').reset_index(drop=True)

        last = df_ej.iloc[-1]
        first = df_ej.iloc[0]

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Peso actual", f"{last['weight']} kg", f"{last['weight']-first['weight']:+.1f}")
        with col2:
            st.metric("Reps actuales", int(last['reps']), f"{int(last['reps'])-int(first['reps']):+d}")

        st.divider()

        # Grafico peso
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_ej['date'], y=df_ej['weight'],
            mode='lines+markers',
            line=dict(color='#1a1a1a', width=2),
            marker=dict(size=7, color='#1a1a1a')
        ))
        fig.update_layout(
            title="Peso (kg)", height=230,
            margin=dict(l=0, r=0, t=32, b=0),
            xaxis=dict(showgrid=False, tickfont=dict(size=10)),
            yaxis=dict(showgrid=True, gridcolor='#f0f0f0', tickfont=dict(size=10)),
            plot_bgcolor='white', paper_bgcolor='white'
        )
        st.plotly_chart(fig, use_container_width=True)

        # Grafico reps
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=df_ej['date'], y=df_ej['reps'],
            mode='lines+markers',
            line=dict(color='#999', width=2),
            marker=dict(size=7, color='#999')
        ))
        fig2.update_layout(
            title="Reps", height=230,
            margin=dict(l=0, r=0, t=32, b=0),
            xaxis=dict(showgrid=False, tickfont=dict(size=10)),
            yaxis=dict(showgrid=True, gridcolor='#f0f0f0', tickfont=dict(size=10)),
            plot_bgcolor='white', paper_bgcolor='white'
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.divider()
        st.subheader("⏱️ Tiempo en cada carga")

        periodos = []
        f_inicio = df_ej.iloc[0]['date']
        p_ref, r_ref = df_ej.iloc[0]['weight'], int(df_ej.iloc[0]['reps'])

        for i, row in df_ej.iterrows():
            if row['weight'] != p_ref or int(row['reps']) != r_ref:
                dias = (row['date'] - f_inicio).days
                periodos.append({
                    'Carga': f"{p_ref}kg × {r_ref}",
                    'Desde': f_inicio.strftime('%d/%m/%y'),
                    'Días': dias
                })
                p_ref, r_ref, f_inicio = row['weight'], int(row['reps']), row['date']

        dias_actual = (df_ej.iloc[-1]['date'] - f_inicio).days
        periodos.append({'Carga': f"{p_ref}kg × {r_ref}", 'Desde': f_inicio.strftime('%d/%m/%y'), 'Días': dias_actual})

        st.dataframe(pd.DataFrame(periodos), use_container_width=True, hide_index=True)
        st.info(f"Llevas **{dias_actual} días** con **{p_ref}kg × {r_ref} reps**")


# ══════════════════════════════════════════
# TAB 4 — HISTORIAL
# ══════════════════════════════════════════
with tab4:
    logs = get_logs()
    if not logs:
        st.info("Sin historial")
    else:
        df = pd.DataFrame(logs)
        df['date'] = pd.to_datetime(df['date'])

        filtro = st.selectbox("Filtrar", ["Todos"] + sorted(df['exercise_name'].unique().tolist()), label_visibility="collapsed")
        if filtro != "Todos":
            df = df[df['exercise_name'] == filtro]

        df_v = df[['date','exercise_name','weight','reps','rir','is_dropset','notes']].copy()
        df_v['date'] = df_v['date'].dt.strftime('%d/%m/%y')
        df_v['is_dropset'] = df_v['is_dropset'].map({True: '🔴', False: ''})
        df_v['rir'] = df_v['rir'].apply(lambda x: f"{int(x)}" if pd.notna(x) else '')
        df_v.columns = ['Fecha','Ejercicio','kg','Reps','RIR','DS','Notas']

        st.caption(f"{len(df_v)} registros")
        st.dataframe(df_v, use_container_width=True, hide_index=True, height=400)
        st.download_button("📥 Descargar CSV", data=df_v.to_csv(index=False),
                           file_name=f"gym_{datetime.now().strftime('%Y%m%d')}.csv",
                           mime="text/csv", use_container_width=True)


# ══════════════════════════════════════════
# TAB 5 — RUTINA
# ══════════════════════════════════════════
with tab5:
    st.subheader("Mis ejercicios")
    st.caption("Ejercicios disponibles para registrar")

    routines = get_routines()
    if routines:
        for r in routines:
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"**{r['exercise_name']}**")
            with col2:
                if st.button("✕", key=f"del_{r['exercise_name']}"):
                    remove_routine(r['exercise_name'])
                    st.cache_data.clear()
                    st.rerun()
    else:
        st.info("Sin ejercicios todavía")

    st.divider()
    new_ex = st.text_input("Nuevo ejercicio", placeholder="Ej: Press de Banca")
    if st.button("Agregar a mi rutina", type="primary"):
        if new_ex.strip():
            try:
                add_routine(new_ex.strip())
                st.cache_data.clear()
                st.success(f"✓ {new_ex} agregado")
                st.rerun()
            except:
                st.error("Ya existe ese ejercicio")
        else:
            st.error("Escribe el nombre")
