import streamlit as st
import pandas as pd
import sqlite3

# CONEXÃO COM O BANCO DE DADOS
conn = sqlite3.connect('../data/quotes.db')

# CARREGAR OS DADOS DA TABELA 'mercadolivre_items' EM UM DATAFRAME PANDAS
df = pd.read_sql_query('SELECT * FROM mercadolivre_items', conn)

# FECHAR CONEXÃO COM BANCO DE DADOS
conn.close()

# TÍTULO DA APLICAÇÃO
st.title('Pesquisa de Mercado - Tênis Esportivos no Mercado Livre')

# MELHORAR O LAYOUT COM COLUNAS PARA KPIs
st.subheader('KPIs principais do sistema')
# st.write(df)

col1, col2, col3 =st.columns(3)

# KPI 1: Número total de itens
total_itens = df.shape[0]
col1.metric(label='Número total de Itens', value=total_itens)

# KPI 2: Número de marcas únicas
unique_brands = df['brand'].nunique()
col2.metric(label='Número de marcas únicas', value=unique_brands)

# KPI 3: Preço Médio novo (em reais)
average_new_price = df['new_price'].mean()
col3.metric(label='Preço Médio Novo (R$)', value=f'{average_new_price:.2f}')

# QUAIS AS MARCAS SÃO MAIS ENCONTRADAS ATÉ A 10ª PÁGINA
st.subheader('Marcas mais encontradas até a 10ª página')
col1, col2 = st.columns([4, 2])

top_10_pages_brands = df['brand'].value_counts().sort_values(ascending=False)
col1.bar_chart(top_10_pages_brands)
col2.write(top_10_pages_brands)

# QUAL PREÇO MÉDIO POR MARCA
st.subheader('Preço Médio por Marca')
col1, col2 = st.columns([4, 2])

avarege_price_by_brand = df.groupby('brand')['new_price'].mean().sort_values(ascending=False)
avarege_price_by_brand = avarege_price_by_brand.round(2)

col1.bar_chart(avarege_price_by_brand)
col2.write(avarege_price_by_brand)

# QUAL A SATISFAÇÃO POR MARCA
st.subheader('Satisfação por marca')
col1, col2 = st.columns([4, 2])

df_non_zero_reviews = df[ df['reviews_rating_number'] > 0 ]
satisfaction_by_brand = df_non_zero_reviews.groupby('brand')['reviews_rating_number'].mean().sort_values(ascending=False)
satisfaction_by_brand = satisfaction_by_brand.round(2)

col1.bar_chart(satisfaction_by_brand)
col2.write(satisfaction_by_brand)