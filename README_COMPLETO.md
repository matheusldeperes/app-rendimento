# 📊 Sistemas SATTE ALAM MOTORS

Coleção de aplicativos Streamlit para gestão operacional da SATTE ALAM MOTORS.

## 📦 Aplicativos Disponíveis

| App | Arquivo | Descrição |
|-----|---------|-----------|
| 📊 **Avaliação e PDI** | `app.py` | Gestão de performance e desenvolvimento individual |
| 💰 **Vendas - Banco Rendimento** | `app_vendas.py` | Controle de comissões de vendas |

## 🚀 Instalação Rápida

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Rodar Sistema de Avaliação e PDI
streamlit run app.py

# OU

# 2. Rodar Sistema de Vendas
streamlit run app_vendas.py
```

## 📚 Documentação Completa

- 📄 [README Principal](README_ORIGINAL.md) - Sistema de Avaliação e PDI
- 💰 [README Vendas](README_VENDAS.md) - Sistema de Vendas - Banco Rendimento
- 🔧 [Configuração Google Sheets](SETUP_GOOGLE_SHEETS.md)
- 🆘 [Solução de Problemas](TROUBLESHOOTING.md)

---

## 📊 Sistema de Avaliação e PDI

### Funcionalidades Principais
- ✅ Formulário de avaliação com 9 critérios (escala 1-5)
- ✅ Plano de Desenvolvimento Individual (PDI)
- ✅ Feedbacks sob demanda
- ✅ Relatórios e gráficos de performance
- ✅ Integração com Google Sheets

### Como Usar
```bash
streamlit run app.py
```

**Planilha Google Sheets:**
- Nome: "Avaliações PDI - SATTE ALAM"
- Aba: "Avaliações" e "Feedbacks"

---

## 💰 Sistema de Vendas - Banco Rendimento

### Funcionalidades Principais
- ✅ Registro de vendas (Consultor, OS, NF, Retorno)
- ✅ Cálculo automático de comissões: `(NF × retorno%) × 0.75`
- ✅ Visualização com filtros por consultor
- ✅ Relatórios de comissões por consultor
- ✅ Exportação em CSV

### Como Usar
```bash
streamlit run app_vendas.py
```

**Planilha Google Sheets:**
- Nome: "Vendas - Banco Rendimento"
- Aba: "Vendas"

### Tabela de Comissões

| Retorno | Percentual | Comissão Líquida |
|---------|-----------|------------------|
| R0 | 0% | 0% |
| R2 | 2% | 1,5% |
| R4 | 4% | 3% |
| R6 | 6% | 4,5% |
| R8 | 8% | 6% |
| R10 | 10% | 7,5% |

**Exemplo:** NF de R$ 10.000 com R10 → Comissão = R$ 750

---

## 🔐 Configuração do Google Sheets

Ambos os apps utilizam as mesmas credenciais do Google Cloud:

### 1. Desenvolvimento Local
Arquivo: `service_account.json`

### 2. Deploy (Streamlit Cloud)
Arquivo: `.streamlit/secrets.toml`

```toml
[gcp_service_account]
type = "service_account"
project_id = "seu-projeto"
# ... demais configurações
```

**Importante:** As planilhas são separadas e não interferem entre si.

---

## 📦 Dependências

```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
gspread>=5.12.0
google-auth>=2.23.0
google-auth-oauthlib>=1.1.0
google-auth-httplib2>=0.1.1
```

---

## 🎨 Identidade Visual

Ambos os apps seguem a identidade visual da SATTE ALAM MOTORS:
- Cores: Preto (#000000), Laranja (#FF6600)
- Fonte: Montserrat
- Suporte a temas light/dark

---

## 🔧 Estrutura do Projeto

```
APP-Rendimento/
├── app.py                          # Sistema de Avaliação e PDI
├── app_vendas.py                   # Sistema de Vendas
├── requirements.txt                # Dependências Python
├── service_account.json           # Credenciais Google (não commitar)
├── logo.png                       # Logo SATTE ALAM
├── .streamlit/
│   └── secrets.toml              # Secrets para deploy
├── README.md                      # Este arquivo
├── README_VENDAS.md              # Documentação detalhada Vendas
└── SETUP_GOOGLE_SHEETS.md        # Guia de configuração
```

---

## 💡 Fluxo de Trabalho

### Sistema de Avaliação
1. Gestor acessa `app.py`
2. Preenche avaliação do colaborador
3. Registra PDI e observações
4. Dados salvos no Google Sheets
5. Consulta relatórios de performance

### Sistema de Vendas
1. Consultor fecha venda com Banco Rendimento
2. Acessa `app_vendas.py`
3. Registra dados da venda
4. Sistema calcula comissão automaticamente
5. Gestor consulta relatórios
6. Contabilidade totaliza no Google Sheets

---

## ⚠️ Segurança

- ⚠️ **Não commitar** `service_account.json` no Git
- ⚠️ Adicionar ao `.gitignore`
- ⚠️ Configurar permissões adequadas no Google Sheets
- ⚠️ Usar secrets do Streamlit Cloud para deploy

---

## 🆘 Suporte e Problemas

### Erros Comuns

**ModuleNotFoundError:**
```bash
pip install -r requirements.txt
```

**Erro de Autenticação Google:**
- Verificar `service_account.json`
- Compartilhar planilhas com email da Service Account

**Planilha não encontrada:**
- Verificar nome da planilha no código
- Criar manualmente se necessário

Consulte `TROUBLESHOOTING.md` para mais detalhes.

---

## 📞 Contato

**SATTE ALAM MOTORS**  
Desenvolvido em: Fevereiro de 2026  
Versão: 2.0

---

## 📄 Licença

Uso interno exclusivo da SATTE ALAM MOTORS.
