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
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from banco_de_dados import salvar_oferta, iniciar_banco

TAG_AFILIADO = "elyad96-20"

# --- CONFIGURAÇÕES ---
MAX_PRODUTOS_POR_CATEGORIA = 12
MAX_TENTATIVAS_POR_CATEGORIA = 2
PASTA_DEBUG = "debug"
MAX_DEBUG_POR_CATEGORIA = 5  # evita acumular lixo no disco
MAX_CATEGORIAS_EM_PARALELO = 3  # cada uma abre seu próprio Chrome; 3 é um bom equilíbrio

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


def configurar_navegador(driver_path):
    """Cria uma instância de Chrome isolada. Cada thread/categoria usa a sua própria,
    reaproveitando o mesmo driver_path (já baixado uma única vez antes de paralelizar)."""
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(f"--user-agent={random.choice(USER_AGENTS)}")
    servico = Service(driver_path)
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


def _texto_para_float(texto):
    """Converte 'R$ 1.299,90' -> 1299.90"""
    limpo = texto.replace("R$", "").replace("\xa0", "").strip()
    limpo = limpo.replace(".", "").replace(",", ".")
    return float(limpo)


def extrair_preco_atual(p):
    """Lê o preço COM centavos.

    Cuidado: a classe 'a-price-whole' contém apenas a parte inteira ('89,'), e os
    centavos ficam em 'a-price-fraction'. Usar só a primeira descarta os centavos e
    faz todo preço virar redondo. A fonte confiável é o span 'a-offscreen' dentro de
    'a-price', que traz o valor completo ('R$ 89,90'); as outras duas classes servem
    de reserva caso a Amazon mude o layout."""
    container = p.find("span", class_="a-price")
    if container:
        offscreen = container.find("span", class_="a-offscreen")
        if offscreen and offscreen.text.strip():
            try:
                return _texto_para_float(offscreen.text)
            except Exception:
                pass

    inteiro_tag = p.find("span", class_="a-price-whole")
    if not inteiro_tag:
        return None
    texto_inteiro = inteiro_tag.text.strip().rstrip(",.").replace(".", "")

    fracao_tag = p.find("span", class_="a-price-fraction")
    centavos = fracao_tag.text.strip() if fracao_tag else "00"

    try:
        return float(f"{texto_inteiro}.{centavos}")
    except Exception:
        return None


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

                    preco_atual = extrair_preco_atual(p)
                    if preco_atual is None:
                        continue

                    preco_original = 0.0
                    preco_antigo_container = p.find("span", class_="a-text-price")
                    if preco_antigo_container:
                        texto_offscreen = preco_antigo_container.find("span", class_="a-offscreen")
                        if texto_offscreen:
                            preco_temp = _texto_para_float(texto_offscreen.text)
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


def _coletar_categoria_isolada(nome_categoria, url_alvo, driver_path):
    """Abre um Chrome próprio para essa categoria, coleta e fecha. Usado por cada worker
    da thread pool — cada categoria roda isolada, sem compartilhar navegador com as outras."""
    driver = configurar_navegador(driver_path)
    try:
        return coletar_categoria(driver, nome_categoria, url_alvo)
    except Exception as e:
        log.error(f"Falha não tratada em {nome_categoria}: {e}")
        return 0
    finally:
        driver.quit()


def rodar_coleta():
    iniciar_banco()
    log.info("🤖 Robô Dicas da Ely iniciado.")

    # Baixa/valida o chromedriver uma única vez antes de abrir os navegadores em paralelo,
    # evitando que várias threads tentem baixar o mesmo driver ao mesmo tempo.
    driver_path = ChromeDriverManager().install()

    resumo = {}
    resumo_lock = threading.Lock()

    with ThreadPoolExecutor(max_workers=MAX_CATEGORIAS_EM_PARALELO) as executor:
        futuros = {
            executor.submit(_coletar_categoria_isolada, nome, url, driver_path): nome
            for nome, url in LISTA_CATEGORIAS.items()
        }
        for futuro in as_completed(futuros):
            nome_categoria = futuros[futuro]
            qtd = futuro.result()
            with resumo_lock:
                resumo[nome_categoria] = qtd

    log.info("✅ Coleta finalizada.")
    # Mantém a ordem original de LISTA_CATEGORIAS no resumo, mesmo com execução paralela
    for cat in LISTA_CATEGORIAS:
        qtd = resumo.get(cat, 0)
        status = "⚠️ ZERO ITENS" if qtd == 0 else f"{qtd} itens"
        log.info(f"   - {cat}: {status}")

    if any(qtd == 0 for qtd in resumo.values()):
        log.warning("Uma ou mais categorias retornaram zero itens. Verifique a pasta 'debug/' e o coleta.log.")


if __name__ == "__main__":
    rodar_coleta()
