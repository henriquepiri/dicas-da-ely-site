import sqlite3
c = sqlite3.connect("estoque_ofertas.db").cursor()
c.execute("SELECT link_afiliado FROM produtos")
links = [r[0] or "" for r in c.fetchall()]
nova = sum(1 for l in links if "dicasdaely05-20" in l)
velha = sum(1 for l in links if "elyad96-20" in l)
print(f"tag nova: {nova} | tag antiga: {velha} | total: {len(links)}")
