from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import random
import re
import os
import glob
import logging
from datetime import datetime
from banco_de_dados import salvar_oferta, iniciar_banco

TAG_AFILIADO = "elyad96-20"

# --- CONFIGURAÇÕES ---
MAX_PRODUTOS_POR_CATEGORIA = 12
MAX_TENTATIVAS_POR_CATEGORIA = 2
PASTA_DEBUG = "debug"
MAX_DEBUG_POR_CATEGORIA = 5  # evita acumular lixo no disco

LISTA_CATEGORIAS = {
    "Mundo do Bebê": "https://www.amazon.com.br/s?k=roupas+brinquedos+seguranca+bebe&i=baby-products",
    "Cozinha": "https://www.amazon.com.br/s?k=organizadores+utensilios+cozinha&i=kitchen",
    "Tecnologia": "https://www.amazon.com.br/s?k=gadgets+inteligentes+casa&i=electronics",
    "Casa & Decor": "https://www.amazon.com.br/s?k=organizacao+casa+decoracao&i=kitchen",
    "Cuidados Pessoais": "https://www.amazon.com.br/s?k=skincare+beleza&i=beauty"
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
]

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("coleta.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("robo_dicas")


def configurar_navegador():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(f"--user-agent={random.choice(USER_AGENTS)}")
    servico = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=servico, options=chrome_options)


def extrair_asin(url):
    try:
        if "/dp/" in url:
            return url.split("/dp/")[1].split("/")[0]
        elif "/product/" in url:
            return url.split("/product/")[1].split("/")[0]
        return None
    except Exception:
        return None


def extrair_parcelas(soup_produto):
    """Lê o texto 'em até 10x' e retorna o número 10"""
    try:
        spans = soup_produto.find_all("span", string=re.compile(r"até \d+x"))
        for s in spans:
            match = re.search(r"(\d+)x", s.text)
            if match:
                return int(match.group(1))
    except Exception:
        pass
    return 1  # Padrão se não achar nada


def salvar_artefatos_debug(driver, nome_categoria):
    """Salva HTML + screenshot da página quando uma categoria falha, para diagnóstico.
    Mantém apenas os N mais recentes por categoria para não acumular lixo."""
    try:
        os.makedirs(PASTA_DEBUG, exist_ok=True)
        slug = re.sub(r'[^a-z0-9]+', '-', nome_categoria.lower()).strip('-')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base = os.path.join(PASTA_DEBUG, f"erro_{slug}_{timestamp}")

        with open(f"{base}.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        driver.save_screenshot(f"{base}.png")

        log.warning(f"Artefatos de debug salvos: {base}.html / {base}.png")

        # Rotaciona: mantém só os MAX_DEBUG_POR_CATEGORIA mais recentes
        for ext in ("html", "png"):
            arquivos = sorted(
                glob.glob(os.path.join(PASTA_DEBUG, f"erro_{slug}_*.{ext}")),
                key=os.path.getmtime,
                reverse=True
            )
            for antigo in arquivos[MAX_DEBUG_POR_CATEGORIA:]:
                os.remove(antigo)
    except Exception as e:
        log.error(f"Falha ao salvar artefatos de debug para {nome_categoria}: {e}")


def coletar_categoria(driver, nome_categoria, url_alvo):
    """Coleta uma categoria, com retry em caso de zero resultados. Retorna a quantidade salva."""
    for tentativa in range(1, MAX_TENTATIVAS_POR_CATEGORIA + 1):
        log.info(f"Visitando {nome_categoria} (tentativa {tentativa}/{MAX_TENTATIVAS_POR_CATEGORIA})...")
        try:
            driver.get(url_alvo)
            time.sleep(random.uniform(3.5, 5.5))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(random.uniform(1.5, 2.5))

            soup = BeautifulSoup(driver.page_source, "html.parser")
            produtos = soup.find_all("div", attrs={"data-component-type": "s-search-result"})
            log.info(f"{nome_categoria}: {len(produtos)} itens encontrados na página.")

            if not produtos:
                log.warning(f"{nome_categoria}: 0 itens na tentativa {tentativa}.")
                salvar_artefatos_debug(driver, nome_categoria)
                if tentativa < MAX_TENTATIVAS_POR_CATEGORIA:
                    time.sleep(random.uniform(4, 7))
                    continue
                return 0

            count = 0
            erros_item = 0
            for p in produtos:
                if count >= MAX_PRODUTOS_POR_CATEGORIA:
                    break
                try:
                    h2 = p.find("h2")
                    titulo = h2.text.strip()

                    preco_atual_tag = p.find("span", class_="a-price-whole")
                    if not preco_atual_tag:
                        continue
                    preco_atual = float(preco_atual_tag.text.replace(".", "").replace(",", "."))

                    preco_original = 0.0
                    preco_antigo_container = p.find("span", class_="a-text-price")
                    if preco_antigo_container:
                        texto_offscreen = preco_antigo_container.find("span", class_="a-offscreen")
                        if texto_offscreen:
                            valor_limpo = texto_offscreen.text.replace("R$", "").replace(".", "").replace(",", ".").strip()
                            preco_temp = float(valor_limpo)
                            if preco_temp > preco_atual:
                                preco_original = preco_temp

                    parcelas = extrair_parcelas(p)

                    nota = "4.5"
                    nota_tag = p.find("span", class_="a-icon-alt")
                    if nota_tag:
                        nota = nota_tag.text.split(" ")[0].replace(",", ".")

                    img_tag = p.find("img", class_="s-image")
                    imagem = img_tag['src']

                    link_tag = p.find("a", class_="a-link-normal s-no-outline")
                    link_completo = f"https://amazon.com.br{link_tag['href']}&tag={TAG_AFILIADO}"

                    asin = extrair_asin(link_completo)
                    if asin:
                        salvar_oferta(asin, titulo, preco_atual, preco_original, link_completo, imagem, nome_categoria, nota, parcelas)
                        count += 1
                except Exception as e:
                    erros_item += 1
                    log.debug(f"{nome_categoria}: item ignorado ({e})")
                    continue

            if erros_item:
                log.info(f"{nome_categoria}: {erros_item} itens ignorados por erro de parsing (seletor pode ter mudado).")

            return count

        except Exception as e:
            log.error(f"Erro na seção {nome_categoria} (tentativa {tentativa}): {e}")
            salvar_artefatos_debug(driver, nome_categoria)
            if tentativa < MAX_TENTATIVAS_POR_CATEGORIA:
                time.sleep(random.uniform(4, 7))

    return 0


def rodar_coleta():
    iniciar_banco()
    driver = configurar_navegador()
    log.info("🤖 Robô Dicas da Ely iniciado.")

    resumo = {}
    try:
        for nome_categoria, url_alvo in LISTA_CATEGORIAS.items():
            qtd = coletar_categoria(driver, nome_categoria, url_alvo)
            resumo[nome_categoria] = qtd
            time.sleep(random.uniform(1, 2))
    finally:
        driver.quit()

    log.info("✅ Coleta finalizada.")
    for cat, qtd in resumo.items():
        status = "⚠️ ZERO ITENS" if qtd == 0 else f"{qtd} itens"
        log.info(f"   - {cat}: {status}")

    if any(qtd == 0 for qtd in resumo.values()):
        log.warning("Uma ou mais categorias retornaram zero itens. Verifique a pasta 'debug/' e o coleta.log.")


if __name__ == "__main__":
    rodar_coleta()
