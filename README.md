# 📊 Sistema de Avaliação e PDI - SATTE ALAM MOTORS

Aplicativo Streamlit para gestão de performance e desenvolvimento individual dos colaboradores.

## 🚀 Instalação

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Rodar o aplicativo
```bash
streamlit run app.py
```

O app abrirá automaticamente no navegador em `http://localhost:8501`

## 📋 Funcionalidades

### 1. **📝 Nova Avaliação**
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
- Salvar automaticamente em arquivo JSON

### 2. **👥 Visualizar Colaboradores**
- Ver lista completa de colaboradores registrados
- Selecionar colaborador para visualizar detalhes
- Editar informações
- **Deletar colaborador** (remover do banco de dados)
- Visualizar gráfico de radar com performance por critério
- Consultar PDI individual

### 3. **📊 Relatório Geral**
- Dashboard com resumo de performance
- Métricas gerais (total de colaboradores, média de pontos, quantidade em alto desempenho)
- **Gráfico de Distribuição de Pontuações**: Visualiza o score de cada colaborador em barras coloridas
- **Curva de Vitalidade**: Histograma com distribuição normal dos scores
  - Linhas de referência para as faixas de classificação
- Tabela resumida de todos os colaboradores (ordenada por pontuação)
- Análise por critério: média de notas em cada um dos 7 critérios

## 📊 Critérios de Classificação

| Pontuação | Classificação | Descrição |
|-----------|---------------|-----------|
| **31-35** | 🟢 ALTO DESEMPENHO | Candidato à promoção/bonificação (Top 20%) |
| **16-30** | 🟡 MANUTENÇÃO | Colaborador estável, necessita ajustes (Médios 60%) |
| **< 16** | 🔴 RISCO | Performance crítica, requer ação (Base 20%) |

## 💾 Armazenamento de Dados

Todos os dados são salvos automaticamente em um arquivo JSON:
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

## 🎯 Como Usar

### Primeira avaliação
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

## 🔧 Requisitos de Sistema

- Python 3.8+
- Acesso ao navegador
- ~50MB de espaço livre

## 📱 Uso Local

O app é executado **apenas localmente** no seu computador. Os dados são armazenados localmente e não são enviados para nenhum servidor externo.

Para rodar em outro computador, basta copiar:
- `app.py`
- `requirements.txt`
- `avaliacoes_pdi.json` (dados existentes, opcional)

## 🎨 Interface

- **Layout responsivo**: Adapta-se a diferentes tamanhos de tela
- **Tema visual**: Gradientes roxos e cores para facilitar leitura
- **Gráficos interativos**: Use Plotly para zoom, pan, etc.
- **Emojis**: Interface amigável e intuitiva

## 💡 Dicas

- Salve regularmente as avaliações
- Faça backup do arquivo `avaliacoes_pdi.json` periodicamente
- Use o PDI para registrar planos de desenvolvimento
- Revise o relatório mensal para acompanhar tendências

## ⚠️ Limitações

- Dados armazenados apenas em JSON (não é um banco de dados robusto)
- Sem sistema de login/autenticação
- Sem histórico de alterações
- Use apenas para gestão local

---

**Desenvolvido para: SATTE ALAM MOTORS**
**Data: Fevereiro de 2026**
# app-rendimento
