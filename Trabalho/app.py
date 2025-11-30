import streamlit as st
import mysql.connector
import pandas as pd
from comparador import ComparadorPrecos
from banco import salvar_no_banco

from banco import salvar_no_banco

# =======================
# Conexão com o MySQL
# =======================
def conectar_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="scraping"
    )

st.set_page_config(page_title="Busca de Livros", layout="centered")
st.title("📚 Consulta de Livros Scrapeados")

# Campo de pesquisa
busca = st.text_input("Pesquisar livro por nome:")

# Botão de pesquisa
if st.button("Buscar"):
    if busca.strip() == "":
        st.warning("Digite o nome do livro.")
    else:
        conexao = None
        cursor = None
        try:
            conexao = conectar_mysql()
            cursor = conexao.cursor(dictionary=True)

            sql = "SELECT site, nome, preco FROM produtos WHERE nome LIKE %s"
            cursor.execute(sql, (f"%{busca}%",))
            resultados = cursor.fetchall()

            if resultados:
                df = pd.DataFrame(resultados)
                st.success(f"{len(df)} livros encontrados!")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Nenhum resultado encontrado no banco. Iniciando scraping…")
                comparador = ComparadorPrecos()

                with st.spinner("Coletando dados, aguarde…"):
                    dados_scraping = comparador.comparar_precos(
                        busca,
                        sites=[
                            'estantevirtual',
                            'dragonstorebrasil',
                            'travessa',
                            'americanas',
                            'amazon',
                            'mercadolivre',
                            'livrariascuritiba',
                            'audible',
                            'magalu'
                        ]
                    )
                comparador.fechar()

                salvar_no_banco(dados_scraping)
                df = pd.DataFrame(dados_scraping)
                st.success(f"{len(df)} livros coletados via scraping!")
                st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Erro: {e}")
        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()
