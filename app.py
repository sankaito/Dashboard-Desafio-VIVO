import streamlit as st
import pandas as pd
import plotly.express as px

# ======================================
# CONFIGURAÇÃO DA PÁGINA
# ======================================

st.set_page_config(
    page_title="Dashboard Logístico",
    page_icon="🚚",
    layout="wide"
)

# ======================================
# CSS CUSTOMIZADO
# ======================================

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.metric-card {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
}

h1 {
    color: #4B0082;
}

</style>
""", unsafe_allow_html=True)

# ======================================
# DADOS
# ======================================

dados = [
    [301, "RotaMax", "Sudeste", 3, 7],
    [302, "ViaCargo", "Sul", 5, 5],
    [303, "FlashLog", "Nordeste", 4, 9],
    [304, "RotaMax", "Norte", 6, 4],
    [305, "ViaCargo", "Centro-Oeste", 2, 6],
    [306, "FlashLog", "Sul", 5, 12],
    [307, "RotaMax", "Sul", 6, 9],
    [308, "ViaCargo", "Sudeste", 3, 4],
    [309, "FlashLog", "Norte", 5, 5],
    [310, "ViaCargo", "Nordeste", 4, 8]
]

df = pd.DataFrame(
    dados,
    columns=[
        "id_entrega",
        "transportadora",
        "regiao",
        "prazo_dias",
        "dias_reais"
    ]
)

# ======================================
# TRATAMENTO
# ======================================

df["dias_atraso"] = (
    df["dias_reais"] - df["prazo_dias"]
).clip(lower=0)

df["status"] = df["dias_atraso"].apply(
    lambda x: "Atrasada" if x > 0 else "No Prazo"
)

# ======================================
# CABEÇALHO
# ======================================

st.title("🚚 Dashboard de Monitoramento Logístico")

st.markdown(
"""
Monitoramento operacional em tempo real das entregas,
identificando atrasos, regiões críticas e desempenho das transportadoras.
"""
)

st.divider()

# ======================================
# FILTROS
# ======================================

st.sidebar.title("🔎 Filtros")

transportadoras = st.sidebar.multiselect(
    "Transportadora",
    options=df["transportadora"].unique(),
    default=df["transportadora"].unique()
)

regioes = st.sidebar.multiselect(
    "Região",
    options=df["regiao"].unique(),
    default=df["regiao"].unique()
)

status = st.sidebar.multiselect(
    "Status",
    options=df["status"].unique(),
    default=df["status"].unique()
)

df_filtrado = df[
    (df["transportadora"].isin(transportadoras))
    & (df["regiao"].isin(regioes))
    & (df["status"].isin(status))
]

# ======================================
# KPIs
# ======================================

total = len(df_filtrado)

atrasadas = len(
    df_filtrado[df_filtrado["status"] == "Atrasada"]
)

percentual = (
    (atrasadas / total) * 100
    if total > 0 else 0
)

dias_total = df_filtrado["dias_atraso"].sum()

maior_atraso = (
    df_filtrado["dias_atraso"].max()
    if total > 0 else 0
)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Entregas", total)
c2.metric("Entregas Atrasadas", atrasadas)
c3.metric("% Atraso", f"{percentual:.1f}%")
c4.metric("Dias Atrasados", dias_total)
c5.metric("Maior Atraso", f"{maior_atraso} dias")

st.divider()

# ======================================
# GRÁFICOS
# ======================================

col1, col2 = st.columns(2)

with col1:

    atrasos_regiao = (
        df_filtrado[df_filtrado["status"] == "Atrasada"]
        .groupby("regiao")
        .size()
        .reset_index(name="Quantidade")
    )

    fig_regiao = px.bar(
        atrasos_regiao,
        x="regiao",
        y="Quantidade",
        color="Quantidade",
        title=" Atrasos por Região",
        text_auto=True,
        color_continuous_scale="Reds"
    )

    fig_regiao.update_layout(
        xaxis_title="Região",
        yaxis_title="Quantidade"
    )

    st.plotly_chart(fig_regiao, width="stretch")

with col2:

    atrasos_transp = (
        df_filtrado[df_filtrado["status"] == "Atrasada"]
        .groupby("transportadora")
        .size()
        .reset_index(name="Quantidade")
    )

    fig_transp = px.bar(
        atrasos_transp,
        x="transportadora",
        y="Quantidade",
        color="Quantidade",
        title=" Comparação entre Transportadoras",
        text_auto=True,
        color_continuous_scale="Blues"
    )

    st.plotly_chart(fig_transp, width="stretch")

# ======================================
# RANKING
# ======================================

st.subheader(" Ranking das entregas mais críticas")

ranking = (
    df_filtrado[df_filtrado["dias_atraso"] > 0]
    .sort_values(
        by="dias_atraso",
        ascending=False
    )
)

st.dataframe(
    ranking[
        [
            "id_entrega",
            "transportadora",
            "regiao",
            "dias_atraso"
        ]
    ],
    width="stretch"
)

# ======================================
# TABELA COMPLETA
# ======================================

st.subheader("📋 Detalhamento")

def colorir_linha(row):

    if row["dias_atraso"] >= 5:
        cor = "#ff6b6b"

    elif row["dias_atraso"] >= 3:
        cor = "#ffd166"

    elif row["dias_atraso"] > 0:
        cor = "#fff3b0"

    else:
        cor = ""

    return [f"background-color: {cor}"] * len(row)

st.dataframe(
    df_filtrado.style.apply(
        colorir_linha,
        axis=1
    ),
    width="stretch"
)

# ======================================
# INSIGHT AUTOMÁTICO
# ======================================

st.divider()

st.subheader("📈 Insight")

if len(ranking) > 0:

    pior = ranking.iloc[0]

    st.error(
        f"""
        Entrega mais crítica encontrada:

        • ID: {pior['id_entrega']}
        • Transportadora: {pior['transportadora']}
        • Região: {pior['regiao']}
        • Atraso: {pior['dias_atraso']} dias

        Recomendação:
        Priorizar investigação operacional dessa entrega.
        """
    )

else:

    st.success(
        "Nenhuma entrega atrasada encontrada."
    )

# ======================================
# RODAPÉ
# ======================================

st.markdown("---")

st.caption(
    "Dashboard desenvolvido para monitoramento logístico e apoio à tomada de decisão."
)

st.markdown("---")

st.caption(
    "Dashboard desenvolvido por SIDS."
)