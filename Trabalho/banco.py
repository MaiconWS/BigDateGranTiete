import mysql.connector

def conectar_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="scraping"
    )

def salvar_no_banco(dados):
    conexao = conectar_mysql()
    cursor = conexao.cursor()

    for item in dados:
        sql = """
        INSERT INTO produtos (site, nome, preco)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE preco = VALUES(preco)
        """
        valores = (item["site"], item["produto"], item["preco"])
        cursor.execute(sql, valores)

    conexao.commit()
    cursor.close()
    conexao.close()
