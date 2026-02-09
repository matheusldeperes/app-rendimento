# 📊 Sistemas SATTE ALAM MOTORS

Coleção de aplicativos Streamlit para gestão operacional da SATTE ALAM MOTORS.

## 📦 Aplicativos Disponíveis

### 1. 📊 Sistema de Avaliação e PDI (`app.py`)
Gestão de performance e desenvolvimento individual dos colaboradores.

### 2. 💰 Sistema de Vendas - Banco Rendimento (`app_vendas.py`)
Registro e controle de comissões de vendas com pagamento via Banco Rendimento.

## 🚀 Instalação

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Rodar os aplicativos

**Sistema de Avaliação e PDI:**
```bash
streamlit run app.py
```

**Sistema de Vendas - Banco Rendimento:**
```bash
streamlit run app_vendas.py
```

Cada app abrirá automaticamente no navegador em `http://localhost:8501`

---

## 📊 SISTEMA DE AVALIAÇÃO E PDI

### 📋 Funcionalidades

#### 1. **📝 Nova Avaliação**
- Preencher dados do colaborador (nome, avaliador, data)
- Avaliar 7 critérios em escala de 1-5:
  - **Comportamental**: Organização, Trabalho em Equipe, Comunicação e Regras
  - **Operacional**: Eficiência Técnica, Qualidade (Retorno)
  - **Processos**: Adesão aos Processos
  - **Evolução**: Capacitação
- Adicionar observações para cada critério
- Preencher Plano de Desenvolvimento Individual (PDI):
  - Pontos fortes (o que continuar fazendo)
  - Gargalos (o que parar de fazer)
  - Ações de melhoria (o que começar a fazer)
- Salvar automaticamente no Google Sheets

#### 2. **👥 Visualizar Colaboradores**
- Ver lista completa de colaboradores registrados
- Selecionar colaborador para visualizar detalhes
- Editar informações
- **Deletar colaborador** (remover do banco de dados)
- Visualizar gráfico de radar com performance por critério
- Consultar PDI individual

#### 3. **📊 Relatório Geral**
- Dashboard com resumo de performance
- Métricas gerais (total de colaboradores, média de pontos, quantidade em alto desempenho)
- **Gráfico de Distribuição de Pontuações**: Visualiza o score de cada colaborador em barras coloridas
- **Curva de Vitalidade**: Histograma com distribuição normal dos scores
  - Linhas de referência para as faixas de classificação
- Tabela resumida de todos os colaboradores (ordenada por pontuação)
- Análise por critério: média de notas em cada um dos 9 critérios

### 📊 Critérios de Classificação

| Pontuação | Classificação | Descrição |
|-----------|---------------|-----------|
| **31-35** | 🟢 ALTO DESEMPENHO | Candidato à promoção/bonificação (Top 20%) |
| **16-30** | 🟡 MANUTENÇÃO | Colaborador estável, necessita ajustes (Médios 60%) |
| **< 16** | 🔴 RISCO | Performance crítica, requer ação (Base 20%) |

### 💾 Armazenamento de Dados

Todos os dados são salvos automaticamente no Google Sheets:
```
avaliacoes_pdi.json
```

O arquivo fica no mesmo diretório do app e persiste entre execuções, permitindo que você:
- Acesse os dados mesmo após fechar o app
- Faça backup do arquivo
- Compartilhe com outros gestores

### Estrutura do arquivo JSON
```json
{
  "Colaborador_2026-02-01": {
    "nome": "João Silva",
    "avaliador": "Gestor X",
    "data": "2026-02-01",
    "scores": {
      "Organização": 4,
      "Trabalho em Equipe": 5,
      ...
    },
    "observacoes": {...},
    "total_pontos": 28,
    "classificacao": "🟡 MANUTENÇÃO",
    "pontos_fortes": [...],
    "gargalos": [...],
    "acoes_melhoria": [...],
    "timestamp": "2026-02-01T14:30:00"
  }
}
```

---

## 💰 SISTEMA DE VENDAS - BANCO RENDIMENTO

### 📋 Funcionalidades

#### 1. **💵 Nova Venda**
- Registrar dados da venda:
  - Nome do Consultor
  - Número da OS (Ordem de Serviço)
  - Valor da NF (Nota Fiscal)
  - Retorno (R0, R2, R4, R6, R8, R10)
- **Cálculo Automático de Comissão**: `(NF × retorno%) × 0.75`
  - R0 = 0% → sem comissão
  - R2 = 2% → 1,5% de comissão líquida
  - R4 = 4% → 3% de comissão líquida
  - R6 = 6% → 4,5% de comissão líquida
  - R8 = 8% → 6% de comissão líquida
  - R10 = 10% → 7,5% de comissão líquida
- Salvar automaticamente no Google Sheets

#### 2. **📊 Visualizar Vendas**
- Tabela com todas as vendas registradas
- Filtro por consultor (seleção múltipla)
- Colunas: Consultor, Nº OS, Valor NF, Retorno, Comissão, Data
- Exportar dados em CSV

#### 3. **📈 Relatório de Comissões**
- **Métricas gerais**: Total de vendas, Valor total NF, Total de comissões, Número de consultores
- **Gráficos**:
  - Vendas por consultor (barras)
  - Comissões por consultor (barras com escala de cores)
  - Distribuição por retorno (pizza)
- **Tabela resumida**: Total NF, Total Comissão e Ticket Médio por consultor
- **Análise por retorno**: Distribuição de comissões pelos diferentes percentuais

### 💾 Armazenamento de Dados

Todos os dados são salvos automaticamente no Google Sheets:
- **Planilha**: "Vendas - Banco Rendimento"
- **Aba**: "Vendas"
- **Cabeçalhos filtráveis**: ID, Nome Consultor, Número OS, Valor NF, Retorno, Percentual Comissão, Valor Comissão, Data Registro, Timestamp
- Os dados são sincronizados em tempo real com o Google Drive

### 💡 Fórmula de Comissão

```
Valor Comissão = (Valor NF × Percentual Retorno) × 0.75
```

**Exemplo:**
- Valor NF: R$ 10.000,00
- Retorno: R10 (10%)
- Cálculo: (10.000 × 10%) × 0.75 = 1.000 × 0.75 = **R$ 750,00**

A fórmula subtrai 25% do valor calculado do retorno.

---

## 🎯 Como Usar

### Sistema de Avaliação e PDI

#### Primeira avaliação
1. Clique em **"📝 Nova Avaliação"** no menu lateral
2. Preencha dados básicos
3. Avalie cada critério de 1 a 5
4. Adicione observações e PDI
5. Clique em **"💾 Salvar Avaliação"**

### Gerenciar colaboradores
1. Acesse **"👥 Visualizar Colaboradores"**
2. Selecione o colaborador desejado
3. Visualize gráficos e informações
4. Ou clique **"🗑️ Deletar"** para remover

### Analisar performance geral
1. Acesse **"📊 Relatório"**
2. Visualize gráficos de distribuição
3. Consulte a curva de vitalidade
4. Analise média por critério

### Sistema de Vendas - Banco Rendimento

#### Registrar uma venda
1. Clique em **"💵 Nova Venda"** no menu lateral
2. Preencha os dados:
   - Nome do Consultor
   - Número da OS
   - Valor da NF
   - Retorno (dropdown)
3. Visualize o cálculo automático da comissão
4. Clique em **"💾 SALVAR VENDA"**

#### Visualizar vendas
1. Acesse **"📊 Visualizar Vendas"**
2. Use filtros por consultor
3. Baixe dados em CSV se necessário

#### Consultar relatórios
1. Acesse **"📈 Relatório de Comissões"**
2. Visualize métricas gerais
3. Analise gráficos por consultor
4. Consulte resumo com totais por consultor

---

## 🔧 Requisitos de Sistema

- Python 3.8+
- Acesso ao navegador
- ~50MB de espaço livre

## 📱 Uso e Armazenamento

Os apps são executados localmente no seu computador, mas os **dados são salvos no Google Sheets** (nuvem).

### Arquivos necessários:
- `app.py` - Sistema de Avaliação e PDI
- `app_vendas.py` - Sistema de Vendas - Banco Rendimento
- `requirements.txt` - Dependências
- `service_account.json` - Credenciais do Google Cloud (não compartilhar)
- `.streamlit/secrets.toml` - Configurações (opcional, para deploy)

### Planilhas criadas no Google Sheets:
1. **"Avaliações PDI - SATTE ALAM"** - Dados de avaliações
2. **"Vendas - Banco Rendimento"** - Dados de vendas e comissões

## 🎨 Interface

- **Layout responsivo**: Adapta-se a diferentes tamanhos de tela
- **Tema visual**: Gradientes roxos e cores para facilitar leitura
- **Gráficos interativos**: Use Plotly para zoom, pan, etc.
- **Emojis**: Interface amigável e intuitiva

## 💡 Dicas

### Sistema de Avaliação e PDI:
- Realize avaliações periódicas (trimestrais recomendado)
- Use o PDI para planos de desenvolvimento de médio/longo prazo
- Revise o relatório mensal para acompanhar tendências
- Utilize os feedbacks sob demanda quando necessário

### Sistema de Vendas:
- Registre vendas imediatamente após o fechamento
- Use filtros para contabilizar comissões por consultor
- Exporte relatórios mensais em CSV para arquivo
- Configure cabeçalhos filtráveis no Google Sheets para facilitar buscas

## ⚠️ Limitações

- Sem sistema de login/autenticação (qualquer pessoa com acesso pode editar)
- Dados dependem de conexão com Google Sheets
- Sem histórico de alterações/versões
- Credenciais do Google devem ser mantidas em segurança

---

## 🔐 Configuração do Google Sheets

Para conectar os apps ao Google Sheets, siga as instruções em `SETUP_GOOGLE_SHEETS.md`.

**Resumo:**
1. Criar projeto no Google Cloud Platform
2. Ativar Google Sheets API e Google Drive API
3. Criar Service Account e baixar credenciais JSON
4. Compartilhar planilhas com o email da Service Account

---

**Desenvolvido para: SATTE ALAM MOTORS**  
**Data: Fevereiro de 2026**  
**Versão: 2.0**
