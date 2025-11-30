from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


class ComparadorPrecos:
    def __init__(self):  # ← corrigido: __init__ com dois underlines antes e depois
        options = Options()
        # Descomente a linha abaixo para rodar sem abrir o navegador
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)

    # =====================================================
    # Função auxiliar para tentar scraping e capturar erros
    # =====================================================
    def tentar_scraping(self, site, funcao, produto):
        try:
            return funcao(produto)
        except Exception as e:
            print(f"[ERRO no site {site}] {e}")
            return [{'site': site, 'produto': 'N/A', 'preco': 'Erro'}]

    # =====================
    # TRAVESSA
    # =====================
    def buscar_travessa(self, produto):
        url = f"https://www.travessa.com.br/Busca.aspx?d=1&bt={produto.replace(' ', '%20')}"
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
    # ESTANTE VIRTUAL
    # =====================
    def buscar_estantevirtual(self, produto):
        url = f"https://www.estantevirtual.com.br/busca?nsCat=Natural&q={produto.replace(' ', '%20')}&searchField=titulo-autor"
        self.driver.get(url)
        time.sleep(3)
        dados = []
        produtos = self.driver.find_elements(By.CLASS_NAME, "product-item__info")
        for prod in produtos[:10]:
            try:
                nome = prod.find_element(By.CLASS_NAME, "product-item__header").text
                preco = prod.find_element(By.CLASS_NAME, "product-item__sale-price").text
                dados.append({'site': 'Estantevirtual', 'produto': nome, 'preco': preco})
            except:
                pass
        return dados

    # =====================
    # AUDIBLE
    # =====================
    def buscar_audible(self, produto):
        url = f"https://www.audible.com.br/search?keywords={produto.replace(' ', '+')}"
        self.driver.get(url)
        time.sleep(3)
        dados = []
        produtos = self.driver.find_elements(By.CLASS_NAME, "productListItem")
        for prod in produtos[:10]:
            try:
                nome = prod.find_element(By.XPATH, ".//h3[contains(@class,'bc-heading')]//a").text
                preco = prod.find_element(By.XPATH, ".//span[contains(text(),'R$')]").text
                dados.append({'site': 'Audible', 'produto': nome, 'preco': preco})
            except:
                pass
        return dados

    # =====================
    # DRAGON STORE
    # =====================
    def buscar_dragonstorebrasil(self, produto):
        url = f"https://dragonstorebrasil.com.br/search/?q={produto.replace(' ', '+')}"
        self.driver.get(url)
        time.sleep(3)
        dados = []
        produtos = self.driver.find_elements(By.CSS_SELECTOR, ".js-item-description")
        for prod in produtos[:10]:
            try:
                nome = prod.find_element(By.CSS_SELECTOR, ".js-item-name").text
                preco = prod.find_element(By.CSS_SELECTOR, "span.js-price-display.item-price").text
                dados.append({'site': 'Dragonstorebrasil', 'produto': nome, 'preco': preco})
            except:
                pass
        return dados

    # =====================
    # LIVRARIAS CURITIBA
    # =====================
    def buscar_livrariascuritiba(self, produto):
        url = f"https://www.livrariascuritiba.com.br/{produto.replace(' ', '%20')}"
        self.driver.get(url)
        time.sleep(3)
        dados = []
        produtos = self.driver.find_elements(By.CLASS_NAME, "product-id")
        for prod in produtos[:10]:
            try:
                nome = prod.find_element(By.CLASS_NAME, "box-name").text
                preco = prod.find_element(By.CLASS_NAME, "bestPrice").text
                dados.append({'site': 'LivrariasCuritiba', 'produto': nome, 'preco': preco})
            except:
                pass
        return dados

    # =====================
    # AMAZON
    # =====================
    def buscar_amazon(self, produto):
        url = f"https://www.amazon.com.br/s?k={produto.replace(' ', '+')}"
        self.driver.get(url)
        time.sleep(4)  # Amazon costuma ser mais lenta + tem CAPTCHA
        dados = []
        produtos = self.driver.find_elements(By.CSS_SELECTOR, "div.s-result-item[data-asin]")
        for prod in produtos[:5]:
            try:
                nome = prod.find_element(By.CSS_SELECTOR, "h2 a span").text
                preco_whole = prod.find_element(By.CSS_SELECTOR, ".a-price-whole").text
                preco_fraction = prod.find_element(By.CSS_SELECTOR, ".a-price-fraction").text or "00"
                preco = f"R$ {preco_whole},{preco_fraction}"
                dados.append({'site': 'Amazon', 'produto': nome, 'preco': preco})
            except:
                try:
                    # alguns produtos têm preço diferente
                    preco = prod.find_element(By.CSS_SELECTOR, ".a-price .a-offscreen").get_attribute("textContent")
                    nome = prod.find_element(By.CSS_SELECTOR, "h2 a span").text
                    dados.append({'site': 'Amazon', 'produto': nome, 'preco': preco})
                except:
                    pass
        return dados

    # =====================
    # AMERICANAS (agora parte do grupo Americanas/Magalu, mas ainda tem URL própria)
    # =====================
    def buscar_americanas(self, produto):
        url = f"https://www.americanas.com.br/busca/{produto.replace(' ', '-')}"
        self.driver.get(url)
        time.sleep(3)
        dados = []
        itens = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='product-card']")
        for item in itens[:5]:
            try:
                nome = item.find_element(By.CSS_SELECTOR, "h3").text
                preco = item.find_element(By.CSS_SELECTOR, "[data-testid='price-value']").text
                dados.append({'site': 'Americanas', 'produto': nome, 'preco': preco})
            except:
                pass
        return dados

    # =====================
    # MERCADO LIVRE
    # =====================
    def buscar_mercadolivre(self, produto):
        url = f"https://lista.mercadolivre.com.br/{produto.replace(' ', '-')}"
        self.driver.get(url)
        time.sleep(3)
        dados = []
        cards = self.driver.find_elements(By.CSS_SELECTOR, ".ui-search-result__content")
        for card in cards[:5]:
            try:
                nome = card.find_element(By.CSS_SELECTOR, "h2").text
                preco = card.find_element(By.CSS_SELECTOR, ".andes-money-amount__fraction").text
                centavos = card.find_element(By.CSS_SELECTOR, ".andes-money-amount__cents").text or "00"
                preco = f"R$ {preco},{centavos}"
                dados.append({'site': 'MercadoLivre', 'produto': nome, 'preco': preco})
            except:
                pass
        return dados

    # =====================
    # MAGALU
    # =====================
    def buscar_magalu(self, produto):
        url = f"https://www.magazineluiza.com.br/busca/{produto.replace(' ', '+')}/"
        self.driver.get(url)
        time.sleep(3)
        dados = []
        itens = self.driver.find_elements(By.CSS_SELECTOR, "li[data-testid='product-list-item']")
        for item in itens[:5]:
            try:
                nome = item.find_element(By.CSS_SELECTOR, "h2[data-testid='product-card::name']").text
                preco = item.find_element(By.CSS_SELECTOR, "p[data-testid='price-value']").text
                dados.append({'site': 'Magalu', 'produto': nome, 'preco': preco})
            except:
                pass
        return dados

    # =====================
    # Sistema de rotas (agora dentro da classe!)
    # =====================
    def comparar_precos(self, produto, sites):
        sites_disponiveis = {
            "travessa": self.buscar_travessa,
            "estantevirtual": self.buscar_estantevirtual,
            "audible": self.buscar_audible,
            "dragonstorebrasil": self.buscar_dragonstorebrasil,
            "livrariascuritiba": self.buscar_livrariascuritiba,
            "amazon": self.buscar_amazon,
            "americanas": self.buscar_americanas,
            "mercadolivre": self.buscar_mercadolivre,
            "magalu": self.buscar_magalu
        }
        todos_dados = []
        for site in sites:
            if site in sites_disponiveis:
                dados = self.tentar_scraping(site, sites_disponiveis[site], produto)
                todos_dados.extend(dados)
        return todos_dados

    def fechar(self):
        self.driver.quit()