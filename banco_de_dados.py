import sqlite3

NOME_BANCO = "estoque_ofertas.db"

def conectar():
    # timeout maior + modo WAL: com o robô rodando categorias em paralelo,
    # várias threads podem tentar escrever ao mesmo tempo. Isso evita erros
    # de "database is locked" fazendo a conexão esperar a vez em vez de falhar.
    conn = sqlite3.connect(NOME_BANCO, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def iniciar_banco():
    conn = conectar()
    cursor = conn.cursor()
    
    # Adicionamos a coluna 'parcelas' (Ex: "3" ou "10")
    sql = """
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asin TEXT UNIQUE,
        titulo TEXT,
        preco_atual REAL,
        preco_original REAL,
        link_afiliado TEXT,
        imagem_url TEXT,
        categoria TEXT,
        nota TEXT,
        parcelas INTEGER DEFAULT 1, -- Nova coluna
        data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """
    cursor.execute(sql)
    conn.commit()
    conn.close()
    print("✅ Banco V4 pronto (Com suporte a Parcelas Reais).")

def salvar_oferta(asin, titulo, preco_atual, preco_original, link, imagem, categoria, nota, parcelas):
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        sql = """
        INSERT INTO produtos (asin, titulo, preco_atual, preco_original, link_afiliado, imagem_url, categoria, nota, parcelas)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(asin) DO UPDATE SET
            titulo = excluded.titulo,
            preco_atual = excluded.preco_atual,
            preco_original = excluded.preco_original,
            -- O link PRECISA ser atualizado: ele carrega a tag de afiliado. Sem esta
            -- linha, trocar a tag no robo_coletor.py só valeria para produtos novos, e
            -- os antigos continuariam mandando comissão para a tag antiga.
            link_afiliado = excluded.link_afiliado,
            imagem_url = excluded.imagem_url,
            categoria = excluded.categoria,
            nota = excluded.nota,
            parcelas = excluded.parcelas,
            data_atualizacao = CURRENT_TIMESTAMP
        """
        cursor.execute(sql, (asin, titulo, preco_atual, preco_original, link, imagem, categoria, nota, parcelas))
        conn.commit()
        # print(f"💾 Salvo: {titulo[:10]}... | {parcelas}x") # Descomente para debug
    except Exception as e:
        print(f"❌ Erro ao salvar: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    iniciar_banco()