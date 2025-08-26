import pandas as pd
import numpy as np
import dask.dataframe as dd

dados_vendas = {
    'produto':['Notebook','Mouse','Teclado'],
    'preco':[2500,50,150],
    'quantidade':[2,10,5]
}

df = pd.DataFrame(dados_vendas)

print("Formato da planilha(linhas, colunas): ", df.shape)
print("Colunas da planilha: ", df.columns.tolist())
print("Tipos de dados das colunas: \n", df.dtypes)

df['Valor_total'] = df['preco']*df['quantidade']

print("\nPlanilha com valor total:")

print(df)