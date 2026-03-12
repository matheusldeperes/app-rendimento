import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

creds = Credentials.from_service_account_file('service_account.json', scopes=SCOPES)
client = gspread.authorize(creds)
ws = client.open('Vendas - Banco Rendimento').worksheet('Vendas')

stamp = datetime.now().strftime('%Y%m%d%H%M%S')
row = [
    f'TESTE_TEMP_{stamp}',
    'Teste',
    999999,
    "'3132,19",
    'R2',
    "'2,00",
    "'46,98",
    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    datetime.now().isoformat(),
]

ws.append_row(row, value_input_option='RAW')
records = ws.get_all_records()
last = records[-1]
print({k: (last.get(k), type(last.get(k)).__name__) for k in ['ID', 'Número OS', 'Valor NF', 'Retorno', 'Percentual Comissão', 'Valor Comissão']})
ws.delete_rows(len(ws.get_all_values()))
