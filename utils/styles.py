import streamlit as st


def inject_css() -> None:
    st.markdown("""
<style>
#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 1rem 1rem 5rem 1rem !important;
    max-width: 480px !important;
    margin: auto;
}

/* Tabs */
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

/* Inputs */
input[type="number"], input[type="text"], textarea {
    font-size: 16px !important;
    min-height: 48px !important;
    border-radius: 10px !important;
}

/* Botón primario */
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

/* Number input */
.stNumberInput > label { font-size: 13px !important; font-weight: 500; color: #888; }
.stNumberInput > div > div > div > input {
    font-size: 22px !important;
    font-weight: 700 !important;
    text-align: center !important;
    min-height: 56px !important;
    border-radius: 10px !important;
}

/* Métricas */
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

.badge-ds  { display:inline-block; background:#fff0f0; color:#c0392b; font-size:10px; font-weight:700; padding:2px 7px; border-radius:20px; }
.badge-rir { display:inline-block; background:#f0f4ff; color:#2c5282; font-size:10px; font-weight:700; padding:2px 7px; border-radius:20px; }
.badge-group { display:inline-block; background:#f0fff4; color:#276749; font-size:10px; font-weight:700; padding:2px 7px; border-radius:20px; }

.log-card {
    background: white;
    border: 1px solid #f0f0f0;
    border-radius: 14px;
    padding: 14px 16px;
    margin-bottom: 10px;
}
.log-card .exname { font-size: 15px; font-weight: 700; color: #1a1a1a; }
.log-card .detail { font-size: 13px; color: #888; margin-top: 4px; }
.log-card .note   { font-size: 12px; color: #aaa; margin-top: 6px; font-style: italic; }

.group-header {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #aaa;
    margin: 1.2rem 0 0.4rem 0;
}
</style>
""", unsafe_allow_html=True)
