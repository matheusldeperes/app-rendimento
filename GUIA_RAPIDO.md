# 🚀 Guia Rápido - Sistemas SATTE ALAM

## 📊 Sistema de Avaliação e PDI

### Executar
```bash
streamlit run app.py
```

### Uso Rápido
1. **Nova Avaliação** → Preencher formulário → Salvar
2. **Visualizar Colaboradores** → Selecionar → Ver/Editar
3. **Relatório** → Consultar métricas e gráficos
4. **Feedbacks** → Registrar feedbacks sob demanda

### Planilha
- Nome: "Avaliações PDI - SATTE ALAM"
- Abas: "Avaliações" e "Feedbacks"

---

## 💰 Sistema de Vendas - Banco Rendimento

### Executar
```bash
streamlit run app_vendas.py
```

### Uso Rápido
1. **Nova Venda** → Preencher dados → Salvar
   - Comissão calculada automaticamente
2. **Visualizar Vendas** → Filtrar por consultor → Exportar CSV
3. **Relatório de Comissões** → Ver gráficos e totais

### Planilha
- Nome: "Vendas - Banco Rendimento"
- Aba: "Vendas"

### Fórmula de Comissão
```
Comissão = (NF × retorno%) × 0.75
```

**Exemplo:** NF R$ 10.000 com R10 (10%) = R$ 750

---

## 🔧 Instalação (primeira vez)

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar Google Sheets
# 1. Colocar service_account.json na pasta
# 2. Compartilhar planilhas com email da service account
```

---

## ⚠️ Importante

- **Não commitar** `service_account.json`
- Ambos os apps usam mesmas credenciais
- Planilhas são separadas (não interferem)
- Dados salvos em tempo real no Google Sheets

---

## 📞 Problemas?

### Erro de módulo
```bash
pip install gspread google-auth streamlit pandas plotly
```

### Erro de autenticação
- Verificar `service_account.json`
- Compartilhar planilha com email da service account

### Planilha não encontrada
- Deixar o app criar automaticamente
- Ou criar manualmente no Google Sheets

---

**SATTE ALAM MOTORS | 2026**
