# 💰 Sistema de Vendas - Banco Rendimento

Sistema Streamlit para registro e controle de comissões de vendas com pagamento via Banco Rendimento.

## 🚀 Como Usar

### Executar o aplicativo
```bash
streamlit run app_vendas.py
```

O app abrirá automaticamente no navegador em `http://localhost:8501`

## 📋 Funcionalidades

### 1. **💵 Nova Venda**
- **Campos do formulário:**
  - Nome do Consultor
  - Número da OS (Ordem de Serviço)
  - Valor da NF (Nota Fiscal)
  - Retorno (dropdown: R0, R2, R4, R6, R8, R10)
  
- **Cálculo Automático de Comissão:**
  ```
  Comissão = (Valor NF × Percentual Retorno) × 0.75
  ```
  
  **Tabela de Comissões:**
  | Retorno | Percentual | Comissão Líquida |
  |---------|-----------|------------------|
  | R0 | 0% | 0% |
  | R2 | 2% | 1,5% |
  | R4 | 4% | 3% |
  | R6 | 6% | 4,5% |
  | R8 | 8% | 6% |
  | R10 | 10% | 7,5% |

- **Exemplo de cálculo:**
  - Valor NF: R$ 10.000,00
  - Retorno: R10 (10%)
  - Cálculo: (10.000 × 10%) × 0.75 = 1.000 × 0.75 = **R$ 750,00**

### 2. **📊 Visualizar Vendas**
- Tabela completa com todas as vendas registradas
- Filtro por consultor (seleção múltipla)
- Colunas exibidas:
  - Consultor
  - Nº OS
  - Valor NF
  - Retorno
  - Comissão
  - Data
- **Exportar dados**: Download em formato CSV

### 3. **📈 Relatório de Comissões**
- **Métricas Gerais:**
  - Total de Vendas
  - Valor Total de NFs
  - Total de Comissões
  - Número de Consultores

- **Gráficos:**
  - Vendas por Consultor (barras)
  - Comissões por Consultor (barras coloridas)
  - Distribuição por Retorno (pizza)

- **Tabela Resumida:**
  - Total NF por consultor
  - Total Comissão por consultor
  - Ticket Médio

- **Análise por Retorno:**
  - Quantidade de vendas em cada faixa de retorno
  - Total de comissões por retorno

## 💾 Armazenamento de Dados

Todos os dados são salvos automaticamente no **Google Sheets**.

### Configuração da Planilha
- **Nome da Planilha**: "Vendas - Banco Rendimento"
- **Aba**: "Vendas"
- **Cabeçalhos** (filtráveis):
  1. ID
  2. Nome Consultor
  3. Número OS
  4. Valor NF
  5. Retorno
  6. Percentual Comissão
  7. Valor Comissão
  8. Data Registro
  9. Timestamp

### Integração com Google Sheets
- Utiliza as mesmas credenciais do `app.py` (Sistema de Avaliação)
- Salva em planilha separada (não interfere nos dados de avaliação)
- Sincronização em tempo real com Google Drive
- Cabeçalhos configurados para filtragem fácil

## 🔐 Configuração

### Credenciais do Google Cloud
O app utiliza as mesmas credenciais configuradas para o `app.py`:

1. **Arquivo local** (desenvolvimento):
   - `service_account.json` na raiz do projeto

2. **Streamlit Secrets** (produção):
   - `.streamlit/secrets.toml`
   ```toml
   [gcp_service_account]
   type = "service_account"
   project_id = "seu-projeto"
   private_key_id = "..."
   private_key = "..."
   client_email = "..."
   client_id = "..."
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "..."
   client_x509_cert_url = "..."
   ```

### Nome Personalizado da Planilha (opcional)
Adicione no `secrets.toml`:
```toml
sheet_name_vendas = "Seu Nome Personalizado"
```

## 🎯 Fluxo de Trabalho Recomendado

### Para Consultores
1. Após fechar venda com Banco Rendimento
2. Acessar o app
3. Preencher formulário "Nova Venda"
4. Verificar cálculo automático da comissão
5. Salvar registro

### Para Gestores
1. Acessar "Visualizar Vendas" para consultar registros
2. Usar filtros por consultor
3. Acessar "Relatório de Comissões" para:
   - Ver métricas gerais
   - Analisar performance por consultor
   - Totalizar comissões do período
4. Exportar dados em CSV para processamento de folha

### Para Contabilidade
1. Acessar planilha diretamente no Google Sheets
2. Usar filtros nos cabeçalhos para:
   - Filtrar por consultor
   - Filtrar por período (Data Registro)
   - Filtrar por retorno
3. Totalizar comissões usando fórmulas do Sheets
4. Gerar relatórios mensais

## 💡 Dicas de Uso

### Melhores Práticas
- ✅ Registre vendas imediatamente após fechamento
- ✅ Confira o número da OS antes de salvar
- ✅ Use filtros do Google Sheets para contabilidade
- ✅ Exporte relatórios mensais em CSV para backup
- ✅ Configure permissões adequadas no Google Sheets

### Evite
- ❌ Editar diretamente no Google Sheets (use o app)
- ❌ Compartilhar credenciais (`service_account.json`)
- ❌ Deixar vendas sem registrar

## 📱 Interface

- **Layout responsivo**: Adapta-se a diferentes tamanhos de tela
- **Identidade visual SATTE ALAM**: Cores corporativas (preto, laranja)
- **Tema light/dark**: Automático conforme configuração do Streamlit
- **Gráficos interativos**: Zoom, pan e exportação
- **Cálculo em tempo real**: Comissão atualiza ao mudar valores

## 🔧 Requisitos

- Python 3.8+
- Conexão com internet (para Google Sheets)
- Navegador web moderno
- Credenciais do Google Cloud configuradas

## 📦 Dependências

```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
gspread>=5.12.0
google-auth>=2.23.0
```

## ⚠️ Limitações

- Sem sistema de login/autenticação
- Sem histórico de edições
- Dependente de conexão com Google Sheets
- Sem cálculo de impostos/descontos adicionais

## 🆘 Suporte

Para problemas comuns, consulte:
- `TROUBLESHOOTING.md` - Solução de problemas
- `SETUP_GOOGLE_SHEETS.md` - Configuração do Google Sheets

---

**Desenvolvido para: SATTE ALAM MOTORS**  
**Data: Fevereiro de 2026**  
**Versão: 1.0**
