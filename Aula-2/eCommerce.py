import pandas as pd
import numpy as np
import dask.dataframe as dd

np.random.seed(42)

numero_vendas = 10000

print("Criando dados simulados de e-commerce...")

dados_loja = {
    'id_usuario': np.random.randint(1, 1001, numero_vendas),
    'id_produto': np.random.randint(1, 501, numero_vendas),
    'categoria': np.random.choice(['Eletrônicos', 'Roupas', 'Livros','Casa','Esportes'], numero_vendas),
    'preco': np.random.exponential(50, numero_vendas),
    'quantidade': np.random.randint(1, 5, numero_vendas)
}

df_loja = pd.DataFrame(dados_loja)

df_loja('Valor_total') = df_loja['preco'] * df_loja['quantidade']

print(df_loja.head())

print(f"\nTotal de vendas: {len(df_loja)}")
print(f"Colunas: {df_loja.columns.tolist()}")

print("=== Análises da loja online ===")

print("\n1. Estatísticas dos preços:")