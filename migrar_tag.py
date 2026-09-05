import sqlite3
conn = sqlite3.connect("estoque_ofertas.db")
c = conn.cursor()
c.execute("UPDATE produtos SET link_afiliado = REPLACE(link_afiliado, ?, ?) WHERE link_afiliado LIKE ?",
          ("elyad96-20", "dicasdaely05-20", "%elyad96-20%"))
conn.commit()
print(f"linhas corrigidas: {c.rowcount}")
c.execute("SELECT link_afiliado FROM produtos")
links = [r[0] or "" for r in c.fetchall()]
print("tag nova:", sum(1 for l in links if "dicasdaely05-20" in l))
print("tag antiga:", sum(1 for l in links if "elyad96-20" in l))
conn.close()
