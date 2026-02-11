import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from string import Template
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials

# Configuração da página
st.set_page_config(
    page_title="Sistema de Vendas - Banco Rendimento",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sistema de autenticação
def verificar_login():
    """Verifica credenciais de login"""
    if 'logado' not in st.session_state:
        st.session_state.logado = False
        st.session_state.nivel_acesso = None
        st.session_state.usuario = None

def fazer_login(usuario, senha):
    """Valida credenciais e define nível de acesso"""
    # Credenciais podem ser configuradas em secrets.toml ou aqui
    usuarios = {
        # Consultores - acesso apenas a "Nova Venda"
        "jose": {"senha": "jose123", "nivel": "consultor", "nome": "José"},
        "diulie": {"senha": "diulie123", "nivel": "consultor", "nome": "Diulie"},
        "jonathan": {"senha": "jonathan123", "nivel": "consultor", "nome": "Jonathan"},
        # Gerente - acesso completo
        "gerente": {"senha": "gerente123", "nivel": "gerente", "nome": "Gerente"}
    }
    
    # Tenta carregar do secrets se disponível
    if "usuarios" in st.secrets:
        usuarios.update(dict(st.secrets["usuarios"]))
    
    if usuario in usuarios and usuarios[usuario]["senha"] == senha:
        st.session_state.logado = True
        st.session_state.nivel_acesso = usuarios[usuario]["nivel"]
        st.session_state.usuario = usuarios[usuario]["nome"]
        return True
    return False

def fazer_logout():
    """Faz logout do sistema"""
    st.session_state.logado = False
    st.session_state.nivel_acesso = None
    st.session_state.usuario = None

# Ajuste de cores para Light/Dark do Streamlit
_theme_base = st.get_option("theme.base") or "dark"
_header_bg = "linear-gradient(135deg, #FFFFFF 0%, #1a1a1a 100%)" if _theme_base == "dark" else "linear-gradient(135deg, #000000 0%, #F5F5F5 100%)"
_header_text = "#FFFFFF" if _theme_base == "dark" else "#000000"
_header_subtext = "#FFFFFF" if _theme_base == "dark" else "#4c4c4c"
_text_primary = "#BBBBBB" if _theme_base == "dark" else "#000000"
_text_secondary = "#BDBDBD" if _theme_base == "dark" else "#4c4c4c"

# Configuração do Google Sheets
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Função para conectar ao Google Sheets
@st.cache_resource
def conectar_google_sheets():
    """Conecta ao Google Sheets usando credenciais do Streamlit Secrets"""
    try:
        # Tenta carregar credenciais do Streamlit Secrets (para Streamlit Cloud)
        if "gcp_service_account" in st.secrets:
            credentials_dict = dict(st.secrets["gcp_service_account"])
            credentials = Credentials.from_service_account_info(
                credentials_dict,
                scopes=SCOPES
            )
        # Fallback para arquivo local (desenvolvimento)
        elif os.path.exists("service_account.json"):
            credentials = Credentials.from_service_account_file(
                "service_account.json",
                scopes=SCOPES
            )
        else:
            st.error("Credenciais do Google não encontradas!")
            st.info("Configure as credenciais em .streamlit/secrets.toml ou service_account.json")
            st.stop()
        
        client = gspread.authorize(credentials)
        return client
    except Exception as e:
        st.error(f"Erro ao conectar ao Google Sheets: {str(e)}")
        st.stop()

# Função para obter ou criar planilha de vendas
@st.cache_resource
def obter_planilha_vendas():
    """Obtém ou cria a planilha de vendas - Banco Rendimento"""
    client = conectar_google_sheets()
    
    # Nome da planilha (pode ser configurado)
    sheet_name = st.secrets.get("sheet_name_vendas", "Vendas - Banco Rendimento")
    
    try:
        # Tenta abrir planilha existente
        spreadsheet = client.open(sheet_name)
        st.success(f"Conectado à planilha: {sheet_name}")
    except gspread.exceptions.SpreadsheetNotFound:
        # Cria nova planilha se não existir
        spreadsheet = client.create(sheet_name)
        st.success(f"Nova planilha criada: {sheet_name}")
    
    # Obtém ou cria a primeira aba
    headers = [
        "ID", "Nome Consultor", "Número OS", "Valor NF", "Retorno",
        "Percentual Comissão", "Valor Comissão", "Data Registro", "Timestamp"
    ]

    try:
        worksheet = spreadsheet.worksheet("Vendas")
        current_headers = worksheet.row_values(1)
        if "Nome Consultor" not in current_headers:
            worksheet.update('A1:I1', [headers])
    except:
        worksheet = spreadsheet.add_worksheet(title="Vendas", rows=1000, cols=20)
        # Adiciona cabeçalhos
        worksheet.update('A1:I1', [headers])
    
    return worksheet

# Mapeamento de Retorno para percentual de comissão
RETORNO_MAP = {
    "R0": 0,
    "R2": 2,
    "R4": 4,
    "R6": 6,
    "R8": 8,
    "R10": 10
}

# Função para calcular comissão
def calcular_comissao(valor_nf, retorno_selecionado):
    """
    Calcula a comissão: (NF * retorno%) * 0.75
    Ou seja: (NF * retorno%) - 25% do resultado
    Onde retorno vai de R0 (0%) até R10 (10%)
    """
    if not valor_nf or valor_nf <= 0:
        return 0, 0
    
    percentual = RETORNO_MAP.get(retorno_selecionado, 0)
    valor_base = valor_nf * percentual / 100
    valor_comissao = valor_base * 0.75  # Subtrai 25% do resultado
    
    # Se a comissão for negativa, retorna 0
    if valor_comissao < 0:
        valor_comissao = 0
    
    return percentual, valor_comissao

# Função para carregar dados do Google Sheets
def carregar_dados_vendas():
    """Carrega dados de vendas do Google Sheets e converte para formato dict"""
    try:
        worksheet = obter_planilha_vendas()
        records = worksheet.get_all_records()
        
        # Converter para formato dict
        dados = {}
        for record in records:
            if record.get('ID'):
                id_col = record['ID']
                dados[id_col] = {
                    'nome_consultor': record.get('Nome Consultor', ''),
                    'numero_os': record.get('Número OS', ''),
                    'valor_nf': float(record.get('Valor NF', 0)) if record.get('Valor NF') else 0,
                    'retorno': record.get('Retorno', ''),
                    'percentual_comissao': float(record.get('Percentual Comissão', 0)) if record.get('Percentual Comissão') else 0,
                    'valor_comissao': float(record.get('Valor Comissão', 0)) if record.get('Valor Comissão') else 0,
                    'data_registro': record.get('Data Registro', ''),
                    'timestamp': record.get('Timestamp', '')
                }
        
        return dados
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return {}

# Função para salvar dados no Google Sheets
def salvar_venda(nome_consultor, numero_os, valor_nf, retorno, percentual_comissao, valor_comissao):
    """Salva uma venda no Google Sheets"""
    try:
        worksheet = obter_planilha_vendas()
        records = worksheet.get_all_records()
        
        # Gera ID único
        id_venda = f"{nome_consultor}_{numero_os}_{datetime.now().isoformat()}"
        data_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        row = [
            id_venda,
            nome_consultor,
            numero_os,
            valor_nf,
            retorno,
            percentual_comissao,
            valor_comissao,
            data_registro,
            datetime.now().isoformat()
        ]
        
        worksheet.append_row(row)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar venda: {str(e)}")
        st.warning("⚠️ **Aviso:** Houve um problema ao salvar. Verifique o Google Sheets manualmente.")
        return False

# CSS customizado com identidade visual SATTE ALAM MOTORS
_css_base = """
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
    /* Cores corporativas SATTE ALAM */
    :root {
        --primary-color: #000000;
        --secondary-color: #FFFFFF;
        --accent-color: #FF6600;
        --support-color: #4c4c4c;
        --text-primary: $text_primary;
        --text-secondary: $text_secondary;
        --bg-light: #FAFAFA;
        --border-color: #E0E0E0;
        --header-bg: $header_bg;
        --header-text: $header_text;
        --header-subtext: $header_subtext;
    }
    
    /* Forçar cor de texto no modo dark */
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] *:not(.stButton):not(.status-high):not(.status-medium):not(.status-low) {
        color: $text_primary !important;
    }
    
    /* Fonte personalizada - Montserrat */
    * {
        font-family: 'Montserrat', 'Segoe UI', sans-serif;
    }
    
    body {
        font-family: 'Montserrat', 'Segoe UI', sans-serif;
    }
    
    /* Header section */
    .header-section {
        background: var(--header-bg);
        padding: 40px;
        border-radius: 12px;
        color: var(--header-text);
        margin-bottom: 30px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        display: flex;
        align-items: center;
        gap: 30px;
    }
    
    /* Metric labels: respeitar tema light/dark */
    [data-testid="stMetricLabel"] {
        background-color: transparent;
        color: var(--text-primary);
    }

    [data-testid="stMetricValue"] {
        color: var(--text-primary);
    }
    
    /* Estilo para o container da logo */
    .logo-container {
        background: var(--header-bg);
        padding: 20px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .header-container {
        background: var(--header-bg);
        padding: 20px 30px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #F5F5F5 0%, #FFFFFF 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #FF6600;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        color: var(--text-primary);
    }
    
    /* Section headers */
    .section-header {
        color: var(--text-primary) !important;
        border-bottom: 3px solid #FF6600;
        padding-bottom: 12px;
        margin-bottom: 20px;
        margin-top: 20px;
        font-weight: 700;
        font-size: 1.3rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Forçar cor de texto GLOBALMENTE */
    * {
        color: $text_primary !important;
    }
    
    /* Exceções para manter cores específicas */
    .stButton button {
        color: white !important;
    }
    
    .status-success {
        color: #1B5E20 !important;
    }
    
    .status-warning {
        color: #E65100 !important;
    }
    
    .status-error {
        color: #C62828 !important;
    }

    /* Labels e valores de métricas */
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
    }
    
    /* Status badges */
    .status-success {
        background-color: #E8F5E9;
        color: #1B5E20;
        padding: 10px 18px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        border: 2px solid #4CAF50;
    }
    
    .status-warning {
        background-color: #FFF3E0;
        color: #E65100;
        padding: 10px 18px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        border: 2px solid #FF6600;
    }
    
    .status-error {
        background-color: #FFEBEE;
        color: #C62828;
        padding: 10px 18px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        border: 2px solid #D32F2F;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #FF6600 0%, #E65100 100%);
        color: white;
        border: none;
        font-weight: 600;
        padding: 12px 24px;
        border-radius: 6px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-family: 'Montserrat', sans-serif;
    }
    
    .stButton > button:hover {
        box-shadow: 0 4px 12px rgba(255, 102, 0, 0.4);
        transform: translateY(-2px);
    }
    
    /* Inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        border: 2px solid #E0E0E0 !important;
        border-radius: 6px;
        font-family: 'Montserrat', sans-serif;
        color: var(--text-primary) !important;
        background-color: transparent !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #FF6600 !important;
        box-shadow: 0 0 0 3px rgba(255, 102, 0, 0.1) !important;
    }
    
    /* Divider */
    hr {
        border-color: #E0E0E0;
        margin: 30px 0;
    }
    
    /* DataFrame styling */
    .dataframe {
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Info/Success/Error boxes */
    .stAlert {
        border-radius: 6px;
        margin: 10px 0;
    }
</style>
"""

# Aplicar CSS customizado
st.markdown(
    Template(_css_base).substitute(
        header_bg=_header_bg,
        header_text=_header_text,
        header_subtext=_header_subtext,
        text_primary=_text_primary,
        text_secondary=_text_secondary,
    ),
    unsafe_allow_html=True,
)

# Título principal
st.markdown("""
<style>
.header-wrapper {
    background: var(--header-bg);
    padding: 20px 30px;
    border-radius: 12px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}
.header-text h1 {
    color: var(--header-text);
    margin: 0;
    font-weight: 700;
    font-size: 2rem;
    letter-spacing: 0.5px;
}
.header-text p {
    color: var(--header-subtext);
    margin: 8px 0 0 0;
    font-size: 0.95rem;
    opacity: 0.95;
    font-weight: 400;
}
</style>
<div class="header-wrapper">
    <div style="flex: 1;">
""", unsafe_allow_html=True)

try:
    col_logo, col_text = st.columns([0.8, 3])
    with col_logo:
        st.image("logo.png", width=180)
    with col_text:
        st.markdown("""
        <div class="header-text">
            <h1>SISTEMA DE VENDAS</h1>
            <p>Registro de Comissões - Banco Rendimento | SATTE ALAM MOTORS</p>
        </div>
        """, unsafe_allow_html=True)
except FileNotFoundError:
    st.markdown("""
    <div class="header-text">
        <h1>SISTEMA DE VENDAS</h1>
        <p>Registro de Comissões - Banco Rendimento | SATTE ALAM MOTORS</p>
    </div>
    """, unsafe_allow_html=True)

# Inicializar sistema de login
verificar_login()

# Tela de Login
if not st.session_state.logado:
    st.markdown('<div style="max-width: 400px; margin: 50px auto;">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">🔐 LOGIN</h2>', unsafe_allow_html=True)
    
    usuario = st.text_input("Usuário", key="login_user")
    senha = st.text_input("Senha", type="password", key="login_pass")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Entrar", use_container_width=True):
            if fazer_login(usuario, senha):
                st.success(f"Bem-vindo(a), {st.session_state.usuario}!")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# Sidebar para gerenciar ações (apenas após login)
st.sidebar.title("GERENCIAMENTO")

# Mostrar usuário logado
st.sidebar.markdown(f"**👤 Usuário:** {st.session_state.usuario}")
st.sidebar.markdown(f"**🔑 Nível:** {st.session_state.nivel_acesso.upper()}")
st.sidebar.divider()

# Menu baseado no nível de acesso
if st.session_state.nivel_acesso == "consultor":
    # Consultores veem apenas "Nova Venda"
    modo = "Nova Venda"
    st.sidebar.info("✅ Nova Venda")
    st.sidebar.markdown("🔒 *Outras opções restritas a gerentes*")
else:
    # Gerentes veem todas as opções
    modo = st.sidebar.radio(
        "Selecione a ação:",
        ["Nova Venda", "Visualizar Vendas", "Relatório de Comissões"]
    )

st.sidebar.divider()
if st.sidebar.button("🚪 Sair", use_container_width=True):
    fazer_logout()
    st.rerun()

if modo == "Nova Venda":
    st.markdown('<h2 class="section-header">FORMULÁRIO DE VENDA</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Se for consultor, preencher automaticamente com o nome do usuário logado
        if st.session_state.nivel_acesso == "consultor":
            nome_consultor = st.session_state.usuario
            st.text_input(
                "Nome do Consultor",
                value=nome_consultor,
                disabled=True,
                key="nome_consultor_display"
            )
        else:
            # Se for gerente, permite selecionar qualquer consultor
            nome_consultor = st.selectbox(
                "Nome do Consultor",
                options=["José", "Diulie", "Jonathan"],
                key="nome_consultor"
            )
    
    with col2:
        numero_os = st.text_input(
            "Número da OS",
            key="numero_os",
            placeholder="Ex: OS-2026-001"
        )
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        valor_nf = st.number_input(
            "Valor da NF (R$)",
            key="valor_nf",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )
    
    with col2:
        retorno = st.selectbox(
            "Retorno",
            options=list(RETORNO_MAP.keys()),
            key="retorno",
            help="Selecione o percentual de retorno (comissão)"
        )
    
    st.divider()
    
    # Cálculo automático de comissão
    percentual, valor_comissao = calcular_comissao(valor_nf, retorno)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Percentual de Comissão", f"{percentual}%")
    
    with col2:
        if valor_comissao > 0:
            st.metric("Valor da Comissão", f"R$ {valor_comissao:.2f}")
        else:
            st.metric("Valor da Comissão", "R$ 0,00", delta="Insuficiente")
    
    st.divider()
    
    # Botão para salvar
    if st.button("SALVAR VENDA", use_container_width=True):
        if nome_consultor.strip() and numero_os.strip() and valor_nf > 0:
            if salvar_venda(nome_consultor, numero_os, valor_nf, retorno, percentual, valor_comissao):
                st.success(f"Venda de {nome_consultor} salva com sucesso!")
                st.balloons()
            else:
                st.error("Erro ao salvar a venda. Tente novamente.")
        else:
            st.error("Por favor, preencha todos os campos obrigatórios!")

elif modo == "Visualizar Vendas":
    st.markdown('<h2 class="section-header">VENDAS REGISTRADAS</h2>', unsafe_allow_html=True)
    
    dados_vendas = carregar_dados_vendas()
    
    if not dados_vendas:
        st.info("Nenhuma venda registrada ainda.")
    else:
        # Criar DataFrame com os dados
        dados_lista = []
        for id_venda, dados_venda in dados_vendas.items():
            dados_lista.append({
                "Consultor": dados_venda["nome_consultor"],
                "N° OS": dados_venda["numero_os"],
                "Valor NF": f"R$ {dados_venda['valor_nf']:.2f}",
                "Retorno": dados_venda["retorno"],
                "Comissão": f"R$ {dados_venda['valor_comissao']:.2f}",
                "Data": dados_venda["data_registro"],
                "ID": id_venda
            })
        
        df = pd.DataFrame(dados_lista)
        
        # Filtro por consultor
        consultores = sorted(set(d["Consultor"] for d in dados_lista))
        filtro_consultor = st.multiselect(
            "Filtrar por Consultor",
            options=["Todos"] + consultores,
            default=["Todos"]
        )
        
        # Aplicar filtro
        if "Todos" in filtro_consultor:
            df_filtrado = df
        else:
            df_filtrado = df[df["Consultor"].isin(filtro_consultor)]
        
        # Exibir tabela com filtro
        st.markdown('<h3 class="section-header">Tabela de Vendas</h3>', unsafe_allow_html=True)
        st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
        
        # Baixar em CSV
        csv = df_filtrado.to_csv(index=False)
        st.download_button(
            label="Baixar dados como CSV",
            data=csv,
            file_name=f"vendas_banco_rendimento_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

elif modo == "Relatório de Comissões":
    st.markdown('<h2 class="section-header">RELATÓRIO DE COMISSÕES</h2>', unsafe_allow_html=True)
    
    dados_vendas = carregar_dados_vendas()
    
    if not dados_vendas:
        st.info("Nenhuma venda registrada ainda.")
    else:
        # Preparar dados para relatório
        relatorio_data = []
        for id_venda, dados_venda in dados_vendas.items():
            relatorio_data.append({
                "Consultor": dados_venda["nome_consultor"],
                "Valor NF": dados_venda["valor_nf"],
                "Retorno": dados_venda["retorno"],
                "Comissão": dados_venda["valor_comissao"],
            })
        
        df_relatorio = pd.DataFrame(relatorio_data)
        
        # Métricas gerais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Vendas", len(df_relatorio))
        
        with col2:
            total_nf = df_relatorio["Valor NF"].sum()
            st.metric("Valor Total NF", f"R$ {total_nf:,.2f}")
        
        with col3:
            total_comissoes = df_relatorio["Comissão"].sum()
            st.metric("Total de Comissões", f"R$ {total_comissoes:,.2f}")
        
        with col4:
            num_consultores = df_relatorio["Consultor"].nunique()
            st.metric("Consultores", num_consultores)
        
        st.divider()
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<h3 class="section-header">VENDAS POR CONSULTOR</h3>', unsafe_allow_html=True)
            
            vendas_por_consultor = df_relatorio.groupby("Consultor").size()
            fig1 = px.bar(
                x=vendas_por_consultor.index,
                y=vendas_por_consultor.values,
                labels={"x": "Consultor", "y": "Quantidade de Vendas"},
                color_discrete_sequence=["#FF6600"],
                height=400
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.markdown('<h3 class="section-header">COMISSÕES POR CONSULTOR</h3>', unsafe_allow_html=True)
            
            comissoes_por_consultor = df_relatorio.groupby("Consultor")["Comissão"].sum()
            fig2 = px.bar(
                x=comissoes_por_consultor.index,
                y=comissoes_por_consultor.values,
                labels={"x": "Consultor", "y": "Comissão (R$)"},
                color=comissoes_por_consultor.values,
                color_continuous_scale=["#E65100", "#FF6600", "#4CAF50"],
                height=400
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        st.divider()
        
        # Tabela resumida por consultor
        st.markdown('<h3 class="section-header">RESUMO POR CONSULTOR</h3>', unsafe_allow_html=True)
        
        resumo_consultor = df_relatorio.groupby("Consultor").agg({
            "Valor NF": "sum",
            "Comissão": "sum",
            "Valor NF": "count"  # Contar vendas
        }).reset_index()
        
        resumo_consultor.columns = ["Consultor", "Total NF", "Total Comissão", "Quantidade Vendas"]
        
        # Calcular Ticket Médio corretamente
        resumo_consultor["Ticket Médio"] = resumo_consultor["Total NF"] / resumo_consultor["Quantidade Vendas"]
        resumo_consultor = resumo_consultor.drop("Quantidade Vendas", axis=1)
        resumo_consultor = resumo_consultor.sort_values("Total Comissão", ascending=False)
        
        # Formatar para exibição
        resumo_display = resumo_consultor.copy()
        resumo_display["Total NF"] = resumo_display["Total NF"].apply(lambda x: f"R$ {x:,.2f}")
        resumo_display["Total Comissão"] = resumo_display["Total Comissão"].apply(lambda x: f"R$ {x:,.2f}")
        resumo_display["Ticket Médio"] = resumo_display["Ticket Médio"].apply(lambda x: f"R$ {x:,.2f}")
        
        st.dataframe(resumo_display, use_container_width=True, hide_index=True)
        
        st.divider()
        
        # Distribuição por Retorno
        st.markdown('<h3 class="section-header">DISTRIBUIÇÃO POR RETORNO</h3>', unsafe_allow_html=True)
        
        dist_retorno = df_relatorio.groupby("Retorno").agg({
            "Comissão": ["sum", "count"]
        }).reset_index()
        
        dist_retorno.columns = ["Retorno", "Total Comissão", "Quantidade"]
        dist_retorno = dist_retorno.sort_values("Total Comissão", ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig3 = px.pie(
                dist_retorno,
                values="Total Comissão",
                names="Retorno",
                height=400,
                title="Comissões por Retorno"
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            st.write("")
            st.dataframe(dist_retorno, use_container_width=True, hide_index=True)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #4c4c4c; margin-top: 30px; font-family: 'Montserrat', sans-serif;">
    <p style="margin: 5px 0; font-weight: 700; font-size: 1.1rem;">SATTE ALAM MOTORS</p>
    <p style="margin: 5px 0; font-size: 0.9rem; color: #000000;">Todos os dados são salvos automaticamente no Google Sheets</p>
    <p style="margin: 5px 0; font-size: 0.85rem; color: #4c4c4c;">Sistema de Vendas - Banco Rendimento v1.0 | Desenvolvido com Streamlit</p>
</div>
""", unsafe_allow_html=True)
