import sqlite3
import os
import shutil
import re
from datetime import datetime
from jinja2 import Template

# --- CONFIGURAÇÕES ---
PASTA_SAIDA = "site_publico"
NOME_BANCO = "estoque_ofertas.db"
ARQUIVO_LOGO = "logo_dicas.png"
URL_SITE = "https://dicasdaely.com.br" # Endereço oficial para o Google

# --- 1. CABEÇALHO COM SEO E GOOGLE VERIFICATION ---
HEAD_COMUM = """
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="referrer" content="no-referrer">
    
    <title>{{ titulo_seo }}</title>
    <meta name="description" content="{{ descricao_seo }}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{{ url_atual }}" />
    
    <meta name="google-site-verification" content="XZ1fEqRKrUn7oM1wvqd1fdZylMvsWTCqToSgrvMv4j0" />

    <meta property="og:title" content="{{ titulo_seo }}">
    <meta property="og:description" content="{{ descricao_seo }}">
    <meta property="og:image" content="{{ imagem_og }}">
    <meta property="og:url" content="{{ url_atual }}">
    <meta property="og:type" content="website">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root {
            --cor-fundo: #fdfbf7;
            --cor-texto: #5c4033;
            --cor-primaria: #8c5e4a;
            --cor-destaque: #d35400;
            --cor-card-border: #eee5e0;
        }
        body { background-color: var(--cor-fundo); font-family: 'Nunito', sans-serif; color: var(--cor-texto); }
        .navbar { background: white; box-shadow: 0 4px 15px rgba(92, 64, 51, 0.05); padding: 15px 0; }
        .logo-img { max-height: 85px; transition: 0.3s; }
        .nav-link { color: var(--cor-texto) !important; font-weight: 700; text-transform: uppercase; font-size: 0.9rem; margin: 0 12px; letter-spacing: 0.5px; }
        .nav-link:hover { color: var(--cor-destaque) !important; }
        
        .hero { background: white; padding: 40px 0; text-align: center; border-bottom: 1px solid var(--cor-card-border); margin-bottom: 40px; }
        
        .card-produto { border: 1px solid var(--cor-card-border); border-radius: 12px; background: white; height: 100%; transition: 0.3s; overflow: hidden; display: flex; flex-direction: column; }
        .card-produto:hover { transform: translateY(-5px); box-shadow: 0 12px 24px rgba(140, 94, 74, 0.15); border-color: var(--cor-primaria); }
        
        .img-wrap { height: 200px; width: 100%; display: flex; align-items: center; justify-content: center; padding: 15px; background-color: white; border-bottom: 1px solid #fafafa; }
        .img-wrap img { max-height: 100%; max-width: 100%; object-fit: contain; }
        
        .card-body { padding: 15px; flex-grow: 1; display: flex; flex-direction: column; }
        .categoria-tag { font-size: 0.7rem; background: #f4ece8; color: var(--cor-primaria); padding: 4px 8px; border-radius: 4px; display: inline-block; margin-bottom: 8px; font-weight: 700; text-transform: uppercase; }
        .titulo-prod { font-size: 1rem; font-weight: 700; color: var(--cor-texto); line-height: 1.3; margin-bottom: 8px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
        .estrelas { color: #f39c12; font-size: 0.8rem; margin-bottom: 12px; }
        .preco-antigo { text-decoration: line-through; color: #aab; font-size: 0.85rem; margin-right: 6px; }
        .preco-atual { color: var(--cor-destaque); font-weight: 800; font-size: 1.5rem; }
        .parcelamento { font-size: 0.8rem; color: #888; margin-bottom: 15px; font-weight: 600; }
        
        .btn-comprar { background: var(--cor-primaria); color: white; border: none; border-radius: 50px; padding: 10px; width: 100%; font-weight: 800; margin-top: auto; transition: 0.3s; text-decoration: none; display: block; text-align: center; }
        .btn-comprar:hover { background: var(--cor-destaque); color: white; }
    </style>
</head>
"""

NAVBAR = """
<nav class="navbar navbar-expand-lg sticky-top">
    <div class="container">
        <a class="navbar-brand py-0" href="index.html">
            <img src="logo_dicas.png" alt="Dicas da Ely" class="logo-img">
        </a>
        <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
             <i class="fas fa-bars" style="color: var(--cor-texto); font-size: 1.5rem;"></i>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto align-items-center">
                <li class="nav-item"><a class="nav-link" href="index.html">Início</a></li>
                {% for cat in categorias %}
                <li class="nav-item"><a class="nav-link" href="cat-{{ cat.slug }}.html">{{ cat.nome }}</a></li>
                {% endfor %}
            </ul>
        </div>
    </div>
</nav>
"""

TEMPLATE_VITRINE = """
<!DOCTYPE html>
<html lang="pt-br">
{{ head }}
<body>
    {{ navbar }}

    {% if is_home %}
    <div class="hero">
        <div class="container">
            <h1 class="display-6 fw-bold mb-3" style="color: var(--cor-primaria);">Seleção Especial</h1>
            <p class="text-muted" style="max-width: 600px; margin: auto; font-size: 1.1rem;">
                Ofertas verificadas e seguras da Amazon para o seu Lar e para o Mundo do Bebê.
                Curadoria feita com amor por Elyad & Henrique.
            </p>
        </div>
    </div>
    {% else %}
    <div class="container mt-5 mb-3"></div>
    {% endif %}

    <div class="container pb-5">
        {% if is_home %}
             <div class="d-flex align-items-center mb-4 mt-2 pb-2 border-bottom border-2" style="border-color: #f0e6e0 !important;">
                <h3 class="fw-bold m-0" style="color: var(--cor-texto);">🧸 Mundo do Bebê</h3>
             </div>
             <div class="row g-4 mb-5">
                {% for p in destaques_bebe %}
                    {{ render_card(p) }}
                {% endfor %}
             </div>
             
             <h3 class="fw-bold mb-4 mt-5" style="color: var(--cor-texto);">✨ Mais Achadinhos</h3>
             <div class="row g-4">
                {% for p in outros_produtos %}
                    {{ render_card(p) }}
                {% endfor %}
             </div>
        {% else %}
             <h2 class="fw-bold mb-4 border-bottom pb-2" style="color: var(--cor-primaria);">{{ titulo_secao }}</h2>
             <div class="row g-4">
                {% for p in produtos %}
                    {{ render_card(p) }}
                {% endfor %}
             </div>
        {% endif %}
    </div>

    <footer class="bg-white py-4 mt-5 border-top text-center small">
        <div class="container">
            <img src="logo_dicas.png" style="height: 40px; opacity: 0.6; margin-bottom: 10px;">
            <p class="mb-1 fw-bold text-muted">© 2026 Dicas da Ely | Todos os direitos reservados</p>
            <small class="text-muted d-block">Participante do Programa de Associados da Amazon.</small>
            <p class="mt-2 text-muted" style="font-size: 0.75rem">Última atualização: {{ data_atual }}</p>
        </div>
    </footer>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

MACRO_CARD = """
{% macro render_card(p) %}
<div class="col-6 col-md-4 col-lg-3">
    <div class="card card-produto">
        <div class="img-wrap">
            <img src="{{ p.imagem }}" loading="lazy" alt="{{ p.titulo }}">
        </div>
        <div class="card-body">
            <span class="categoria-tag">{{ p.categoria }}</span>
            <div class="titulo-prod" title="{{ p.titulo }}">{{ p.titulo }}</div>
            
            <div class="estrelas">
                {% for i in range(p.estrelas_int) %} <i class="fas fa-star"></i> {% endfor %}
                <span class="text-muted ms-1 small">({{ p.nota }})</span>
            </div>
            
            <div class="mt-auto">
                {% if p.preco_original_float > p.preco_atual_float %}
                    <span class="preco-antigo">R$ {{ p.preco_original }}</span>
                {% endif %}
                
                <div class="preco-atual">R$ {{ p.preco_atual }}</div>
                
                {% if p.parcelas > 1 %}
                    <div class="parcelamento">Em até {{ p.parcelas }}x sem juros</div>
                {% else %}
                    <div class="parcelamento">À vista</div>
                {% endif %}
                
                <a href="{{ p.link }}" target="_blank" class="btn btn-comprar">
                    Ver na Amazon
                </a>
            </div>
        </div>
    </div>
</div>
{% endmacro %}
"""

# --- FUNÇÕES AUXILIARES ---

def criar_slug(texto):
    s = re.sub(r'[^a-z0-9]+', '-', texto.lower()).strip('-')
    return s if s else "geral"

def formatar_moeda(valor):
    try: return f"{float(valor):.2f}".replace('.', ',')
    except: return valor

def processar_produto(row):
    try:
        p = {
            'titulo': row[0],
            'preco_atual': formatar_moeda(row[1]),
            'preco_atual_float': float(row[1]),
            'preco_original': formatar_moeda(row[2]),
            'preco_original_float': float(row[2]),
            'imagem': row[3],
            'link': row[4],
            'categoria': row[5],
            'nota': row[6],
            'parcelas': row[7]
        }
        # Tratamento de estrelas
        try: p['estrelas_int'] = int(float(row[6]))
        except: p['estrelas_int'] = 5
        return p
    except Exception as e:
        print(f"Erro ao processar linha: {e}")
        return None

def gerar_sitemap(categorias):
    """Gera o arquivo sitemap.xml para o Google encontrar as páginas"""
    print("🗺️  Gerando Sitemap...")
    data_hoje = datetime.now().strftime('%Y-%m-%d')
    
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
   <url>
      <loc>{URL_SITE}/</loc>
      <lastmod>{data_hoje}</lastmod>
      <changefreq>daily</changefreq>
      <priority>1.0</priority>
   </url>
   <url>
      <loc>{URL_SITE}/index.html</loc>
      <lastmod>{data_hoje}</lastmod>
      <changefreq>daily</changefreq>
      <priority>0.8</priority>
   </url>"""
    
    for cat in categorias:
        xml += f"""
   <url>
      <loc>{URL_SITE}/cat-{cat['slug']}.html</loc>
      <lastmod>{data_hoje}</lastmod>
      <changefreq>weekly</changefreq>
      <priority>0.8</priority>
   </url>"""
        
    xml += "\n</urlset>"
    
    with open(f"{PASTA_SAIDA}/sitemap.xml", "w", encoding="utf-8") as f:
        f.write(xml)

def main():
    # 1. Preparar pastas
    if os.path.exists(PASTA_SAIDA): shutil.rmtree(PASTA_SAIDA)
    os.makedirs(PASTA_SAIDA)
    if os.path.exists(ARQUIVO_LOGO): shutil.copy(ARQUIVO_LOGO, os.path.join(PASTA_SAIDA, ARQUIVO_LOGO))

    conn = sqlite3.connect(NOME_BANCO)
    cursor = conn.cursor()
    
    # 2. Pegar categorias
    cursor.execute("SELECT DISTINCT categoria FROM produtos WHERE categoria IS NOT NULL")
    cats_db = sorted([r[0] for r in cursor.fetchall() if r[0]])
    menu_categorias = [{'nome': c, 'slug': criar_slug(c)} for c in cats_db]

    # 3. Preparar templates
    full_template_str = MACRO_CARD + TEMPLATE_VITRINE.replace("{{ head }}", HEAD_COMUM)
    tpl = Template(full_template_str)
    navbar_html = Template(NAVBAR).render(categorias=menu_categorias)
    data_atual_str = datetime.now().strftime('%d/%m/%Y')

    # 4. GERAÇÃO DA HOME (index.html)
    # Busca produtos de bebê
    cursor.execute("SELECT titulo, preco_atual, preco_original, imagem_url, link_afiliado, categoria, nota, parcelas FROM produtos WHERE categoria = 'Mundo do Bebê' ORDER BY id DESC LIMIT 8")
    destaques_bebe = [p for p in [processar_produto(r) for r in cursor.fetchall()] if p]
    
    # Busca outros produtos
    cursor.execute("SELECT titulo, preco_atual, preco_original, imagem_url, link_afiliado, categoria, nota, parcelas FROM produtos WHERE categoria != 'Mundo do Bebê' ORDER BY id DESC LIMIT 40")
    outros_produtos = [p for p in [processar_produto(r) for r in cursor.fetchall()] if p]

    # Renderiza Home
    html_home = tpl.render(
        navbar=navbar_html, 
        is_home=True, 
        # SEO da Home
        titulo_seo="Dicas da Ely | Achadinhos e Ofertas Amazon para Bebê e Casa",
        descricao_seo="Confira nossa seleção de fraldas, itens para enxoval e utilidades domésticas com os melhores preços. Verificado por Elyad & Henrique.",
        imagem_og=f"{URL_SITE}/{ARQUIVO_LOGO}",
        url_atual=f"{URL_SITE}/",
        titulo_pag="Início", 
        destaques_bebe=destaques_bebe, 
        outros_produtos=outros_produtos,
        data_atual=data_atual_str
    )
    with open(f"{PASTA_SAIDA}/index.html", "w", encoding="utf-8") as f: f.write(html_home)

    # 5. GERAÇÃO DAS CATEGORIAS
    for cat in menu_categorias:
        cursor.execute("SELECT titulo, preco_atual, preco_original, imagem_url, link_afiliado, categoria, nota, parcelas FROM produtos WHERE categoria = ?", (cat['nome'],))
        prods_cat = [p for p in [processar_produto(r) for r in cursor.fetchall()] if p]
        
        slug = cat['slug']
        # Renderiza Categoria
        html_cat = tpl.render(
            navbar=navbar_html, 
            is_home=False, 
            # SEO da Categoria
            titulo_seo=f"Ofertas de {cat['nome']} | Dicas da Ely",
            descricao_seo=f"Encontre as melhores promoções de {cat['nome']} selecionadas a dedo na Amazon.",
            imagem_og=f"{URL_SITE}/{ARQUIVO_LOGO}",
            url_atual=f"{URL_SITE}/cat-{slug}.html",
            titulo_secao=cat['nome'], 
            produtos=prods_cat,
            data_atual=data_atual_str
        )
        with open(f"{PASTA_SAIDA}/cat-{slug}.html", "w", encoding="utf-8") as f: f.write(html_cat)

    # 6. Gerar o Sitemap
    gerar_sitemap(menu_categorias)

    conn.close()
    print("✅ SITE GERADO COM SUCESSO!")
    print("   - index.html criado")
    print("   - sitemap.xml criado (Google vai amar)")
    print("   - Páginas de categoria criadas")

if __name__ == "__main__":
    main()