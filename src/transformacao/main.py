import pandas as pd
import sqlite3
from datetime import datetime
import re


def correct_value(val):
    val_str = str(val)
    # Verifica se o valor está no formato '1.600'
    if re.match(r'^\d+\.\d{3}$', val_str):
        val_str = val_str.replace('.', '')
        return float(val_str)
    return val


df = pd.read_json('../data/data.jsonl', lines=True)

# SETAR O PANDAS PARA MOSTRAR TODAS AS COLUNAS
pd.options.display.max_columns = None

# CRIAÇAO DE DUAS NOVAS COLUNAS ['_source] = de onde sairam os dados // ['_data_coleta']
df['_source'] = 'https://lista.mercadolivre.com.br/tenis-corrida-masculino'
df["_data_coleta"] = datetime.now()

df['new_price_reais'] = df['new_price_reais'].apply(correct_value)

# TRATAMENTO DOS DADOS
df['old_price_reais'] = df['old_price_reais'].fillna(0).astype(float)
df['old_price_centavos'] = df['old_price_centavos'].fillna(0).astype(float)
df['new_price_reais'] = df['new_price_reais'].fillna(0).astype(float)
df['new_price_centavos'] = df['new_price_centavos'].fillna(0).astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0).astype(float)

# REMOVER OS PARENTESES DA COLUNA 'review_amount'
df['reviews_amount'] = df['reviews_amount'].str.replace('[\(\)]', '', regex=True)
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)

# TRATAR OS PREÇOS COMO FLOATS E CALCULAR OS VALORES TOTAIS
df['old_price'] = df['old_price_reais'] + df['old_price_centavos'] / 100
df['new_price'] = df['new_price_reais'] + df['new_price_centavos'] / 100

# REMOVER AS COLUNAS ANTIGAS DOS PREÇOS
df.drop(columns=['old_price_reais', 'old_price_centavos', 'new_price_reais', 'new_price_centavos'], inplace=True)

new_order = ['brand', 'name', 'old_price', 'new_price', 'reviews_rating_number', 'reviews_amount', '_data_coleta', '_source']
df = df[new_order]

# CONEXÃO COM O BANCO DE DADOS
conn = sqlite3.connect('../data/quotes.db')

# SALVAR O DataFrame NO BANCO DE DADOS SQLITE
df.to_sql('mercadolivre_items', conn, if_exists='replace', index=False)

# FECHAR CONEXÃO COM O BANCO
conn.close()

# print(df.head())