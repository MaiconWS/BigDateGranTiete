from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import mysql.connector
import time

produto = input("Digite o nome do livro que deseja buscar: ")

# ========================
# 1) CONEXÃO E BANCO MYSQL
# ========================

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

cursor = conexao.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS scraping")
cursor.close()
conexao.close()

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="scraping"
)

cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    site VARCHAR(50),
    nome VARCHAR(255),
    preco VARCHAR(50),
    UNIQUE KEY unique_produto (site, nome)
)
""")

# ==========================
# 2) WEB SCRAPING (CLASSE)
# ==========================

class ComparadorPrecos:
    def __init__(self):
        options = Options()
        # options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)

    # =====================================================
    # Função auxiliar para tentar scraping e capturar erros
    # =====================================================
    def tentar_scraping(self, site, funcao, produto):
        try:
            dados = funcao(produto)
            return dados
        except Exception as e:
            print(f"[ERRO no site {site}] {e}")

            return [{
                'site': site,
                'produto': 'N/A',
                'preco': 'Scraping falhou / site com proteção anti-bot'
            }]

    # =====================
    # TRAVESSA (FUNCIONA)
    # =====================
    def buscar_travessa(self, produto):
        url = f"https://www.travessa.com.br/Busca.aspx?d=1&bt={produto.replace(' ', '%20'),"&cta=00&codtipoartigoexplosao=1"}"
        self.driver.get(url)
        time.sleep(3)

        dados = []
        produtos = self.driver.find_elements(By.CSS_SELECTOR, "div.col-sm-12.col-md-9 .livro")

        for prod in produtos[:10]:
            try:
                nome = prod.find_element(By.CSS_SELECTOR, "search-result-item-heading").text
                preco = prod.find_element(By.CSS_SELECTOR, ".value3").text
                dados.append({'site': 'Travessa', 'produto': nome, 'preco': preco})
            except:
                pass

        return dados

    # =====================
    # ESTANTE 
    # =====================
    def buscar_estantevirtual(self, produto):
        url = f"https://www.estantevirtual.com.br/busca?nsCat=Natural&q={produto.replace(' ', '%20')}&searchField=titulo-autor"
        self.driver.get(url)
        time.sleep(3)

        produtos = self.driver.find_elements(By.CLASS_NAME, "product-item__info")
        dados = []

        for prod in produtos[:10]:
            try:
                nome = prod.find_element(By.CLASS_NAME, "product-item__header").text
                preco = prod.find_element(By.CLASS_NAME, "product-item__sale-price").text
                dados.append({'site': 'Estantevirtual', 'produto': nome, 'preco': preco})
            except:
                pass
        return dados
    
    def buscar_audible(self, produto):
        url = f"https://www.audible.com.br/search?keywords={produto.replace(' ', '+')}"
        self.driver.get(url)
        time.sleep(3)

        produtos = self.driver.find_elements(By.CLASS_NAME, "productListItem")
        dados = []

        for prod in produtos[:10]:
            try:
                nome = prod.find_element(By.XPATH, ".//h3[contains(@class,'bc-heading')]//a").text
                preco = prod.find_element(By.XPATH, ".//span[contains(text(),'R$')]").text
                dados.append({'site': 'Audible', 'produto': nome, 'preco': preco})
            except Exception as e:
                print("Erro no item Audible:", e)
                pass

        return dados

    # =====================
    # DRAGON STORE
    # =====================
    def buscar_dragonstorebrasil(self, produto):
        url = f"https://dragonstorebrasil.com.br/search/?q={produto.replace(' ', '+')}"
        self.driver.get(url)
        time.sleep(3)

        produtos = self.driver.find_elements(By.CSS_SELECTOR, ".js-item-description")
        dados = []

        for prod in produtos[:10]:
            try:
                nome = prod.find_element(By.CSS_SELECTOR, ".js-item-name").text
                preco = prod.find_element(By.CSS_SELECTOR, "span.js-price-display.item-price").text
                dados.append({'site': 'dragonstorebrasil', 'produto': nome, 'preco': preco})
            except:
                pass
        return dados
    
    def buscar_livrariaCuritiba(self, produto):
        url = f"https://www.livrariascuritiba.com.br/{produto.replace(' ', '%20')}"
        self.driver.get(url)
        time.sleep(3)

        produtos = self.driver.find_elements(By.CLASS_NAME, "product-id")
        dados = []

        for prod in produtos[:10]:
            try:
                nome = prod.find_element(By.CLASS_NAME, "box-name").text
                preco = prod.find_element(By.CLASS_NAME, "bestPrice").text
                dados.append({'site': 'livrariascuritiba', 'produto': nome, 'preco': preco})
            except:
                pass
        return dados

    # ======================
    # SITES COM POSSÍVEIS BLOQUEIOS
    # (mas agora eles serão tentados!)
    # ======================

    def buscar_amazon(self, produto):
        url = f"https://www.amazon.com.br/s?k={produto.replace(' ', '+')}"
        self.driver.get(url)
        time.sleep(3)

        produtos = self.driver.find_elements(By.CSS_SELECTOR, "div.s-card-container")
        dados = []

        for prod in produtos[:5]:
            try:
                nome = prod.find_element(By.CSS_SELECTOR, "h2 span").text
                preco = prod.find_element(By.CSS_SELECTOR, ".a-price-whole").text
                dados.append({'site': 'Amazon', 'produto': nome, 'preco': preco})
            except:
                pass

        return dados

    def buscar_americanas_real(self, produto):
        url = f"https://www.americanas.com.br/busca/{produto.replace(' ', '-')}"
        self.driver.get(url)
        time.sleep(3)

        itens = self.driver.find_elements(By.CSS_SELECTOR, ".product-grid-item")
        dados = []

        for item in itens[:5]:
            try:
                nome = item.find_element(By.CSS_SELECTOR, "h3").text
                preco = item.find_element(By.CSS_SELECTOR, ".price__SalesPrice-sc").text
                dados.append({'site': 'Americanas', 'produto': nome, 'preco': preco})
            except:
                pass

        return dados

    def buscar_mercadolivre(self, produto):
        url = f"https://lista.mercadolivre.com.br/{produto.replace(' ', '-')}"
        self.driver.get(url)
        time.sleep(3)

        cards = self.driver.find_elements(By.CSS_SELECTOR, ".ui-search-result__content-wrapper")
        dados = []

        for card in cards[:5]:
            try:
                nome = card.find_element(By.CSS_SELECTOR, "poly-component__title-wrapper").text
                preco = card.find_element(By.CSS_SELECTOR, "poly-price__current").text
                dados.append({'site': 'Mercado Livre', 'produto': nome, 'preco': preco})
            except:
                pass
        return dados

    def buscar_magalu(self, produto):
        url = f"https://www.magazineluiza.com.br/busca/{produto.replace(' ', '+')}/"
        self.driver.get(url)
        time.sleep(3)

        itens = self.driver.find_elements(By.CSS_SELECTOR, "li.sc-gswNZR")
        dados = []

        for item in itens[:5]:
            try:
                nome = item.find_element(By.CSS_SELECTOR, "product-title").text
                preco = item.find_element(By.CSS_SELECTOR, "price-value").text
                dados.append({'site': 'Magalu', 'produto': nome, 'preco': preco})
            except:
                pass
        return dados

    # ======================
    # SISTEMA DE ROTAS
    # ======================
    def comparar_precos(self, produto, sites=None):

        sites_disponiveis = {
            "estantevirtual": self.buscar_estantevirtual,
            "dragonstorebrasil": self.buscar_dragonstorebrasil,
            "travessa": self.buscar_travessa,
            "livrariascuritiba": self.buscar_livrariaCuritiba,
            "audible": self.buscar_audible,

            # sites com bloqueio (agora tentarão rodar)
            "amazon": self.buscar_amazon,
            "americanas": self.buscar_americanas_real,
            "mercadolivre": self.buscar_mercadolivre,
            "magalu": self.buscar_magalu,
        }

        todos_dados = []

        for site in sites:
            print(f"\nBuscando em: {site}")

            if site not in sites_disponiveis:
                print(f"Site '{site}' não reconhecido.")
                continue

            # Agora TENTA rodar e se der erro → retorna fallback automaticamente
            dados = self.tentar_scraping(site, sites_disponiveis[site], produto)
            print(f"{len(dados)} resultados encontrados.")
            todos_dados.extend(dados)

        return todos_dados

    def fechar(self):
        self.driver.quit()


# ===================
# 3) EXECUÇÃO GERAL
# ===================

comparador = ComparadorPrecos()

try:
    produto = produto

    dados = comparador.comparar_precos(
        produto,
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

    df = pd.DataFrame(dados)
    df.to_csv('comparacao_precos.csv', index=False, encoding='utf-8')

    for item in dados:
        sql = """
        INSERT INTO produtos (site, nome, preco)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE preco = VALUES(preco)
        """
        valores = (item['site'], item['produto'], item['preco'])
        cursor.execute(sql, valores)

    conexao.commit()

finally:
    comparador.fechar()
    cursor.close()
    conexao.close()
