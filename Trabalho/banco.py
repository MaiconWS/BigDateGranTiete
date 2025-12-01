import mysql.connector

def criar_banco():
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    cursor = conexao.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS scraping")
    cursor.close()
    conexao.close()

def conectar_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="scraping"
    )

def criar_tabela():
    conexao = conectar_mysql()
    cursor = conexao.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        site VARCHAR(50),
        nome VARCHAR(255),
        preco VARCHAR(50),
        preco_num DECIMAL(10,2),
        UNIQUE KEY unique_produto (site, nome)
)
""")
    conexao.commit()
    cursor.close()
    conexao.close()

def salvar_no_banco(dados):
    conexao = conectar_mysql()
    cursor = conexao.cursor()

    for item in dados:
        sql = """
        INSERT INTO produtos (site, nome, preco_num)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE preco_num = VALUES(preco_num)
        """
        valores = (item["site"], item["produto"], item["preco_num"])
        cursor.execute(sql, valores)

    conexao.commit()
    cursor.close()
    conexao.close()

criar_banco() # garante que o banco exista
criar_tabela() # garante que a tabela exista