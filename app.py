# -*- coding: utf-8 -*-
import copy
import streamlit as st
import plotly.graph_objects as go
from modelo import sistema, pl_unico, pddd

st.set_page_config(page_title="Comparação PL Único x PDDD", page_icon="⚡", layout="wide")

st.markdown("""
<style>
/* TEMA CLARO: não altera posição, opções nem lógica do dashboard */
:root {
    color-scheme: light !important;
}

html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: #ffffff !important;
    color: #0f2747 !important;
}

/* Cabeçalho do Streamlit/GitHub em fundo claro */
[data-testid="stHeader"],
header[data-testid="stHeader"] {
    background-color: #ffffff !important;
    color: #0f2747 !important;
    box-shadow: none !important;
}

[data-testid="stToolbar"],
[data-testid="stToolbar"] button,
[data-testid="stToolbar"] a,
[data-testid="stHeaderActionElements"],
[data-testid="stHeaderActionElements"] button,
[data-testid="stHeaderActionElements"] a {
    background-color: #ffffff !important;
    color: #0f2747 !important;
}

[data-testid="stToolbar"] svg,
[data-testid="stHeaderActionElements"] svg {
    fill: #0f2747 !important;
    color: #0f2747 !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}

/* Barra lateral e controles claros */
[data-testid="stSidebar"],
[data-testid="stSidebarContent"] {
    background-color: #f3f6fa !important;
    border-right: 1px solid #d7e0eb !important;
}

[data-testid="stSidebar"] *,
[data-testid="stSidebarContent"] * {
    color: #0f2747 !important;
}

[data-testid="stNumberInput"] input,
[data-testid="stNumberInput"] div[data-baseweb="input"],
[data-testid="stNumberInput"] div[data-baseweb="input"] > div {
    background-color: #ffffff !important;
    color: #0f2747 !important;
    -webkit-text-fill-color: #0f2747 !important;
}

[data-testid="stNumberInput"] button {
    background-color: #ffffff !important;
    color: #0f2747 !important;
    border-color: #cbd5e1 !important;
}

/* Títulos, textos, mensagens e resultados legíveis */
h1, h2, h3, h4, h5, h6,
p, label, span,
[data-testid="stCaptionContainer"],
[data-testid="stMarkdownContainer"] {
    color: #0f2747 !important;
}

[data-testid="stMetric"] {
    background-color: #f8fafc !important;
    border: 1px solid #d7e0eb !important;
    border-radius: 10px !important;
    padding: 12px !important;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] *,
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] * {
    color: #0f2747 !important;
    opacity: 1 !important;
}

[data-testid="stAlert"] {
    background-color: #eff6ff !important;
    color: #0f2747 !important;
}

/* Abas: mantém posição e opções existentes */
div[data-baseweb="tab-list"] {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 10px !important;
    background-color: #f3f6fa !important;
    border: 1px solid #d7e0eb !important;
    border-radius: 12px !important;
    padding: 8px !important;
    margin-top: 18px !important;
    margin-bottom: 24px !important;
}

button[role="tab"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    background-color: #ffffff !important;
    color: #0f2747 !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
    padding: 10px 18px !important;
    min-height: 42px !important;
    white-space: nowrap !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

button[role="tab"] p,
button[role="tab"] span,
button[role="tab"] div {
    color: #0f2747 !important;
    opacity: 1 !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    margin: 0 !important;
}

button[role="tab"][aria-selected="true"] {
    background-color: #2563eb !important;
    color: #ffffff !important;
    border-color: #2563eb !important;
    box-shadow: 0 2px 6px rgba(37, 99, 235, 0.22) !important;
}

button[role="tab"][aria-selected="true"] p,
button[role="tab"][aria-selected="true"] span,
button[role="tab"][aria-selected="true"] div {
    color: #ffffff !important;
    opacity: 1 !important;
    font-weight: 700 !important;
}

button[role="tab"]:hover {
    background-color: #e8f0fe !important;
    border-color: #2563eb !important;
}

button[role="tab"][aria-selected="true"]:hover {
    background-color: #1d4ed8 !important;
}

div[data-baseweb="tab-highlight"],
div[data-baseweb="tab-border"] {
    display: none !important;
}

div[data-baseweb="tab-panel"] {
    background-color: #ffffff !important;
    color: #0f2747 !important;
    padding-top: 8px !important;
}

/* Expansor e JSON de resultados */
[data-testid="stExpander"],
[data-testid="stExpander"] details,
[data-testid="stExpander"] summary {
    background-color: #ffffff !important;
    color: #0f2747 !important;
}

[data-testid="stJson"],
[data-testid="stJson"] * {
    color: #0f2747 !important;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)


def br(v, c=2):
    return f"{v:,.{c}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def nome(s):
    return s.replace("_", " ").title().replace("Uhe", "UHE").replace("Ute", "UTE")


def layout(fig, titulo, yaxis):
    fig.update_layout(
        title=dict(text=titulo, x=0.01), paper_bgcolor="#fff", plot_bgcolor="#fff",
        hovermode="x unified", height=520,
        margin=dict(l=80, r=190, t=70, b=70),
        legend=dict(orientation="v", x=1.02, xanchor="left", y=1),
        xaxis=dict(title="Estágio mensal", dtick=1, gridcolor="#e2e8f0", automargin=True),
        yaxis=dict(title=yaxis, gridcolor="#e2e8f0", automargin=True),
    )
    return fig


with st.sidebar:
    st.header("Parâmetros da comparação")
    cenario_nome = st.radio("Cenário hidrológico", ["Otimista", "Pessimista"])
    cenario = 0 if cenario_nome == "Otimista" else 1
    carga_pct = st.slider("Carga do sistema (%)", 50, 150, 100, 5)
    st.subheader("Condição inicial")
    volumes = []
    for u in sistema["UHE"]:
        volumes.append(st.number_input(
            f'Volume inicial - {nome(u["Nome"])} (hm³)',
            min_value=float(u["Vmin"]), max_value=float(u["Vmax"]),
            value=float(u["VI"]), step=1.0))
    st.subheader("PDDD")
    tolerancia = st.number_input("Tolerância máxima", 0.0001, 1_000_000.0, 0.01, 0.01, format="%.4f")
    max_iter = st.number_input("Máximo de iterações", 1, 1000, 100, 1)
    executar = st.button("Comparar modelos", type="primary", use_container_width=True)

st.title("Comparação: PL Único × PDDD")
st.caption("Comparação das decisões de geração e armazenamento sob os mesmos dados de entrada.")

if executar:
    sis = copy.deepcopy(sistema)
    sis["DGer"]["Carga"] = [v * carga_pct / 100 for v in sistema["DGer"]["Carga"]]
    for i, v in enumerate(volumes):
        sis["UHE"][i]["VI"] = float(v)
    try:
        with st.spinner("Resolvendo PL Único e PDDD..."):
            r_pl = pl_unico(sis, cenario=cenario, imprime=False)
            r_pd = pddd(sis, cenario=cenario, imprime=False,
                        tolerancia=float(tolerancia), max_iter=int(max_iter))
        st.session_state["comparacao"] = (sis, r_pl, r_pd)
    except Exception as e:
        st.error(f"Falha na comparação: {e}")
        st.stop()

if "comparacao" not in st.session_state:
    st.info("Defina os parâmetros e clique em **Comparar modelos**.")
    st.stop()

sis, r_pl, r_pd = st.session_state["comparacao"]
est = list(range(1, sis["DGer"]["Nr_Est"] + 1))

c1, c2, c3, c4 = st.columns(4)
c1.metric("Custo total | PL Único", f'R$ {br(r_pl["DGer"]["CustoTotal"])}')
c2.metric("Custo total | PDDD", f'R$ {br(r_pd["DGer"]["CustoTotal"])}')
dif = r_pd["DGer"]["CustoTotal"] - r_pl["DGer"]["CustoTotal"]
c3.metric("Diferença PDDD − PL", f'R$ {br(dif)}')
c4.metric("Iterações da PDDD", r_pd["DGer"]["Nr_Iteracoes"])

aba_v, aba_gh, aba_gt, aba_def, aba_conv = st.tabs([
    "Armazenamento", "Geração UHE", "Geração UTE", "Déficit", "Convergência PDDD"
])

with aba_v:
    for i, u in enumerate(sis["UHE"]):
        fig = go.Figure()
        fig.add_scatter(x=est, y=r_pl["UHE"][i]["vf"], name="PL Único",
                        mode="lines+markers", line=dict(color="#2563eb", width=4))
        fig.add_scatter(x=est, y=r_pd["UHE"][i]["vf"], name="PDDD",
                        mode="lines+markers", line=dict(color="#ef4444", width=3, dash="dash"))
        st.plotly_chart(layout(fig, f'Evolução do volume armazenado final — {nome(u["Nome"])}', "Volume final (hm³)"), use_container_width=True, theme=None)

with aba_gh:
    for i, u in enumerate(sis["UHE"]):
        gh_pl = r_pl["UHE"][i].get("gh", [u["Prod"] * v for v in r_pl["UHE"][i]["vt"]])
        gh_pd = [u["Prod"] * v for v in r_pd["UHE"][i]["vt"]]
        fig = go.Figure()
        fig.add_scatter(x=est, y=gh_pl, name="PL Único", mode="lines+markers", line=dict(color="#2563eb", width=4))
        fig.add_scatter(x=est, y=gh_pd, name="PDDD", mode="lines+markers", line=dict(color="#ef4444", width=3, dash="dash"))
        st.plotly_chart(layout(fig, f'Geração hidráulica — {nome(u["Nome"])}', "Geração (MWméd)"), use_container_width=True, theme=None)

with aba_gt:
    for i, u in enumerate(sis["UTE"]):
        fig = go.Figure()
        fig.add_scatter(x=est, y=r_pl["UTE"][i]["gt"], name="PL Único", mode="lines+markers", line=dict(color="#2563eb", width=4))
        fig.add_scatter(x=est, y=r_pd["UTE"][i]["gt"], name="PDDD", mode="lines+markers", line=dict(color="#ef4444", width=3, dash="dash"))
        st.plotly_chart(layout(fig, f'Geração térmica — {nome(u["Nome"])}', "Geração (MWméd)"), use_container_width=True, theme=None)

with aba_def:
    fig = go.Figure()
    fig.add_scatter(x=est, y=r_pl["DGer"]["Deficit"], name="PL Único", mode="lines+markers", line=dict(color="#2563eb", width=4))
    fig.add_scatter(x=est, y=r_pd["DGer"]["Deficit"], name="PDDD", mode="lines+markers", line=dict(color="#ef4444", width=3, dash="dash"))
    st.plotly_chart(layout(fig, "Déficit por estágio", "Déficit (MWméd)"), use_container_width=True, theme=None)

with aba_conv:
    n = min(len(r_pd["DGer"]["ZINF"]), len(r_pd["DGer"]["ZSUP"]))
    it = list(range(1, n + 1))
    fig = go.Figure()
    fig.add_scatter(x=it, y=r_pd["DGer"]["ZINF"][:n], name="ZINF", mode="lines+markers", line=dict(color="#2563eb", width=4))
    fig.add_scatter(x=it, y=r_pd["DGer"]["ZSUP"][:n], name="ZSUP", mode="lines+markers", line=dict(color="#f59e0b", width=4))
    fig.update_layout(xaxis_title="Iteração")
    st.plotly_chart(layout(fig, "Evolução de ZINF e ZSUP", "Custo (R$)"), use_container_width=True, theme=None)

with st.expander("Resultados numéricos"):
    st.subheader("PL Único")
    st.json(r_pl, expanded=False)
    st.subheader("PDDD")
    st.json(r_pd, expanded=False)
