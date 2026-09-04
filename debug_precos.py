from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# --- AJUSTE SE QUISER TESTAR OUTRA CATEGORIA/PRODUTO ---
URL = "https://www.amazon.com.br/s?k=roupas+de+bebe&i=baby-products"
ASIN_ALVO = "B0FDPZ48LT"  # produto "Bichinhos Carinhosos - Loja Era Uma Vez"

chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
servico = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=servico, options=chrome_options)

print(f"Abrindo: {URL}")
driver.get(URL)
try:
    WebDriverWait(driver, 12).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-component-type='s-search-result']"))
    )
except Exception:
    print("Aviso: timeout esperando os cards, seguindo mesmo assim...")

driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
time.sleep(2)

print(f"Titulo da pagina carregada: {driver.title}")
driver.save_screenshot("debug_screenshot.png")
print("Screenshot salvo em debug_screenshot.png (abra esse arquivo pra ver o que o robo esta vendo)")
with open("debug_pagina.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)
print("HTML completo salvo em debug_pagina.html\n")

soup = BeautifulSoup(driver.page_source, "html.parser")
cards = soup.find_all("div", attrs={"data-component-type": "s-search-result"})
print(f"Total de cards encontrados: {len(cards)}\n")

encontrado = False
for card in cards:
    if ASIN_ALVO in str(card):
        encontrado = True
        print("=== CARD DO PRODUTO ALVO ENCONTRADO ===\n")

        h2s = card.find_all("h2")
        print(f"Total de h2 encontrados no card: {len(h2s)}")
        for i, h2_tag in enumerate(h2s):
            print(f"\n[h2 #{i}] classes={h2_tag.get('class')}")
            print(h2_tag.prettify())
        print()

        print("--- TODOS os spans com 'a-price' na classe (nessa ordem, é o que importa) ---")
        for i, tag in enumerate(card.find_all("span", class_=lambda c: c and "a-price" in c)):
            print(f"\n[{i}] classes={tag.get('class')}")
            print(tag.prettify())
        break

if not encontrado:
    print(f"ASIN {ASIN_ALVO} não apareceu nesta coleta (pode ter mudado de posição/pagina). Rode de novo.")

driver.quit()
