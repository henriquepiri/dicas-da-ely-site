from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re # Biblioteca para achar números no texto
from banco_de_dados import salvar_oferta, iniciar_banco

TAG_AFILIADO = "elyad96-20"

# --- NOMES DE CATEGORIA LIMPOS ---
LISTA_CATEGORIAS = {
    "Mundo do Bebê": "https://www.amazon.com.br/s?k=roupas+brinquedos+seguranca+bebe&i=baby-products",
    "Cozinha": "https://www.amazon.com.br/s?k=organizadores+utensilios+cozinha&i=kitchen",
    "Tecnologia": "https://www.amazon.com.br/s?k=gadgets+inteligentes+casa&i=electronics",
    "Casa & Decor": "https://www.amazon.com.br/s?k=organizacao+casa+decoracao&i=kitchen",
    "Cuidados Pessoais": "https://www.amazon.com.br/s?k=skincare+beleza&i=beauty"
}

def configurar_navegador():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    servico = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=servico, options=chrome_options)

def extrair_asin(url):
    try:
        if "/dp/" in url: return url.split("/dp/")[1].split("/")[0]
        elif "/product/" in url: return url.split("/product/")[1].split("/")[0]
        return None
    except: return None

def extrair_parcelas(soup_produto):
    """Lê o texto 'em até 10x' e retorna o número 10"""
    try:
        # Procura spans que contenham "até" e "x de"
        spans = soup_produto.find_all("span", string=re.compile(r"até \d+x"))
        for s in spans:
            # Extrai o número antes do 'x'
            match = re.search(r"(\d+)x", s.text)
            if match:
                return int(match.group(1))
    except:
        pass
    return 1 # Padrão se não achar nada

def rodar_coleta():
    iniciar_banco()
    driver = configurar_navegador()
    print(f"🤖 Robô Dicas da Ely iniciado.")

    for nome_categoria, url_alvo in LISTA_CATEGORIAS.items():
        print(f"\n🌍 Visitando: {nome_categoria}...")
        try:
            driver.get(url_alvo)
            time.sleep(4)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(2)
            
            soup = BeautifulSoup(driver.page_source, "html.parser")
            produtos = soup.find_all("div", attrs={"data-component-type": "s-search-result"})
            
            print(f"📦 Analisando {len(produtos)} itens...")

            count = 0
            for p in produtos:
                try:
                    if count >= 12: break 
                    
                    h2 = p.find("h2")
                    titulo = h2.text.strip()
                    
                    # PREÇO ATUAL
                    preco_atual_tag = p.find("span", class_="a-price-whole")
                    if not preco_atual_tag: continue
                    preco_atual = float(preco_atual_tag.text.replace(".", "").replace(",", "."))
                    
                    # PREÇO ORIGINAL (Correção da Confusão)
                    preco_original = 0.0
                    # O seletor "a-text-price" é específico para preço riscado
                    preco_antigo_container = p.find("span", class_="a-text-price")
                    if preco_antigo_container:
                        texto_offscreen = preco_antigo_container.find("span", class_="a-offscreen")
                        if texto_offscreen:
                            valor_limpo = texto_offscreen.text.replace("R$", "").replace(".", "").replace(",", ".").strip()
                            preco_temp = float(valor_limpo)
                            
                            # PROVA REAL: O preço antigo DEVE ser maior que o atual
                            # Se for menor, é porque pegou o valor da parcela errado
                            if preco_temp > preco_atual:
                                preco_original = preco_temp

                    # PARCELAS (Lê direto do card)
                    parcelas = extrair_parcelas(p)

                    # NOTA
                    nota = "4.5"
                    nota_tag = p.find("span", class_="a-icon-alt")
                    if nota_tag: nota = nota_tag.text.split(" ")[0].replace(",", ".")
                    
                    img_tag = p.find("img", class_="s-image")
                    imagem = img_tag['src']
                    
                    link_tag = p.find("a", class_="a-link-normal s-no-outline")
                    link_completo = f"https://amazon.com.br{link_tag['href']}&tag={TAG_AFILIADO}"
                    
                    asin = extrair_asin(link_completo)
                    if asin:
                        salvar_oferta(asin, titulo, preco_atual, preco_original, link_completo, imagem, nome_categoria, nota, parcelas)
                        count += 1
                except Exception as e: 
                    # print(e) 
                    continue
            
            time.sleep(1)

        except Exception as e:
            print(f"Erro na seção {nome_categoria}: {e}")

    driver.quit()
    print("\n✅ Coleta Finalizada com Sucesso!")

if __name__ == "__main__":
    rodar_coleta()