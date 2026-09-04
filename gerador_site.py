import sqlite3
import os
import shutil
import re
import json
import math
from datetime import datetime
from jinja2 import Template

# --- CONFIGURAÇÕES ---
PASTA_SAIDA = "site_publico"
NOME_BANCO = "estoque_ofertas.db"
ARQUIVO_LOGO = "logo_dicas.png"
URL_SITE = "https://dicasdaely.com.br"
PRODUTOS_POR_PAGINA = 24
GA_MEASUREMENT_ID = "G-JDYT3SLVZJ"  # Propriedade GA4 "Dicas da Ely"
PRODUTOS_ENTRE_DICAS = 8  # a cada N produtos, intercala uma caixinha de dica no grid

# --- CONTEÚDO EDITORIAL POR CATEGORIA ---
# Dicas genéricas de compra (não são resenha de produto específico — é orientação
# de como escolher bem dentro daquela categoria). É isso que dá o tom de "site de
# dicas" em vez de só uma lista de links de afiliado.
CATEGORIA_INFO = {
    "Mundo do Bebê": {
        "intro": "Selecionamos itens para bebê pensando em segurança e custo-benefício. "
                 "Na hora de escolher, fique de olho na faixa etária recomendada pelo fabricante "
                 "e prefira sempre materiais atóxicos e certificados pelo Inmetro.",
        "dicas": [
            "Antes de comprar roupinhas de bebê, confira a tabela de medidas do vendedor — o "
            "tamanho \"RN\" varia bastante entre marcas.",
            "Brinquedos com peças pequenas só são seguros a partir dos 3 anos. Pra bebês menores, "
            "prefira sempre itens maiores que a boca da criança.",
            "Berços, cadeirinhas e carrinhos devem ter selo do Inmetro — é a garantia mínima de "
            "segurança exigida no Brasil.",
        ],
    },
    "Cozinha": {
        "intro": "Aqui reunimos organizadores e utensílios que realmente fazem diferença no dia a "
                 "dia da cozinha — sem gastar mais do que precisa.",
        "dicas": [
            "Potes herméticos de vidro custam mais, mas não mancham nem retêm cheiro como os de "
            "plástico — vale o investimento pra quem guarda tempero e óleo.",
            "Organizadores empilháveis rendem muito mais espaço de armário do que parecem na foto — "
            "meça a prateleira antes de comprar.",
            "Utensílios de silicone aguentam mais calor que os de plástico comum e não risham "
            "panela antiaderente.",
        ],
    },
    "Tecnologia": {
        "intro": "Gadgets pra casa inteligente que valem o preço — testamos a categoria pensando em "
                 "praticidade real, não só em novidade.",
        "dicas": [
            "Antes de comprar qualquer gadget \"inteligente\", confira se ele funciona com o "
            "assistente de voz que você já usa (Alexa, Google Assistente) — nem todos são compatíveis.",
            "Tomadas e lâmpadas inteligentes que usam Wi-Fi direto (sem hub) são mais fáceis de "
            "instalar, mas costumam pesar mais na sua rede — bom pra quem tem poucos dispositivos.",
            "Fios organizadores e réguas com USB parecem bobos, mas resolvem 90% da bagunça de mesa "
            "por menos de R$ 30.",
        ],
    },
    "Casa & Decor": {
        "intro": "Organização e decoração com foco em coisas que resolvem um problema real da casa, "
                 "não só enfeite.",
        "dicas": [
            "Prateleiras e organizadores multiuso costumam caber em mais lugares do que os "
            "específicos pra um cômodo só — pense na flexibilidade antes de comprar.",
            "Fitas dupla-face de montagem removível seguram bem em superfície lisa, mas soltam em "
            "parede com textura ou tinta velha — teste num cantinho antes.",
            "Itens de decoração com tons neutros (bege, terracota, verde-oliva) combinam com mais "
            "ambientes e não saem de moda tão rápido.",
        ],
    },
    "Cuidados Pessoais": {
        "intro": "Achadinhos de skincare e beleza com bom custo-benefício — sempre vale conferir a "
                 "lista de ingredientes se você tem pele sensível.",
        "dicas": [
            "Protetor solar é o item de skincare com melhor custo-benefício a longo prazo — vale "
            "priorizar mesmo com orçamento apertado.",
            "Produtos com ácidos (retinol, vitamina C) devem entrar aos poucos na rotina — comece "
            "usando 2-3x por semana antes de usar todo dia.",
            "Pele oleosa também precisa de hidratante — pular essa etapa costuma piorar a oleosidade, "
            "não melhorar.",
        ],
    },
    "GERAL": {
        "dicas": [
            "Todos os preços aqui são coletados diretamente da Amazon todos os dias — o valor pode "
            "mudar entre nossa última atualização e o momento da sua compra, então confira o preço "
            "final na página do produto.",
            "Somos participantes do Programa de Associados da Amazon: se você compra por um dos "
            "nossos links, a gente recebe uma pequena comissão, sem custo extra pra você.",
        ],
    },
}

# --- 1. CABEÇALHO COM SEO, PERFORMANCE E DADOS ESTRUTURADOS ---
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

    <link rel="icon" type="image/png" href="logo_dicas.png">

    <link rel="preconnect" href="https://cdn.jsdelivr.net">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

    {% if ga_id %}
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={{ ga_id }}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', '{{ ga_id }}');
    </script>
    {% endif %}

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">

    {% if json_ld %}
    <script type="application/ld+json">{{ json_ld }}</script>
    {% endif %}

    <style>
        :root {
            --cor-fundo: #fdfbf7;
            --cor-texto: #5c4033;
            --cor-primaria: #8c5e4a;
            --cor-destaque: #d35400;
            --cor-card-border: #eee5e0;
            --cor-selo: #2e9e5b;
        }
        body { background-color: var(--cor-fundo); font-family: 'Nunito', sans-serif; color: var(--cor-texto); }
        h1, h2, h3, .navbar-brand-text { font-family: 'Baloo 2', 'Nunito', sans-serif; }

        .navbar { background: white; box-shadow: 0 4px 15px rgba(92, 64, 51, 0.05); padding: 15px 0; }
        .logo-img { max-height: 85px; transition: 0.3s; }
        .nav-link { color: var(--cor-texto) !important; font-weight: 700; text-transform: uppercase; font-size: 0.9rem; margin: 0 12px; letter-spacing: 0.5px; }
        .nav-link:hover { color: var(--cor-destaque) !important; }

        .hero { background: linear-gradient(180deg, #fff 0%, var(--cor-fundo) 100%); padding: 48px 0; text-align: center; border-bottom: 1px solid var(--cor-card-border); margin-bottom: 40px; }
        .hero h1 { color: var(--cor-primaria); }
        .selo-confianca { max-width: 720px; margin: 32px auto 0; }
        .selo-confianca .item-selo i { color: var(--cor-primaria); }
        .selo-confianca .item-selo .titulo-selo { font-weight: 800; font-size: 0.85rem; color: var(--cor-texto); }
        .selo-confianca .item-selo .desc-selo { font-size: 0.78rem; color: #a89a90; }

        .card-dica { background: linear-gradient(135deg, #fff7f0, #fdf1e8); border: 1.5px dashed var(--cor-primaria); border-radius: 14px; padding: 20px 22px; height: 100%; display: flex; align-items: flex-start; gap: 14px; }
        .card-dica .icone-dica { font-size: 1.6rem; line-height: 1; flex-shrink: 0; }
        .card-dica .rotulo-dica { font-weight: 800; color: var(--cor-primaria); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; display: block; margin-bottom: 4px; }
        .card-dica p { margin: 0; font-size: 0.88rem; line-height: 1.5; color: var(--cor-texto); }

        .intro-categoria { max-width: 780px; color: #8a7a70; font-size: 0.98rem; margin-bottom: 28px; line-height: 1.55; }

        .card-produto { position: relative; border: 1px solid var(--cor-card-border); border-radius: 14px; background: white; height: 100%; transition: 0.25s ease; overflow: hidden; display: flex; flex-direction: column; }
        .card-produto:hover { transform: translateY(-6px); box-shadow: 0 14px 28px rgba(140, 94, 74, 0.18); border-color: var(--cor-primaria); }

        .badge-desconto { position: absolute; top: 10px; left: 10px; z-index: 2; background: var(--cor-selo); color: white; font-weight: 800; font-size: 0.75rem; padding: 4px 9px; border-radius: 30px; box-shadow: 0 3px 8px rgba(0,0,0,0.15); }

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

        .paginacao .page-link { color: var(--cor-primaria); border-color: var(--cor-card-border); font-weight: 700; }
        .paginacao .page-item.active .page-link { background-color: var(--cor-primaria); border-color: var(--cor-primaria); }

        .empty-state { text-align: center; padding: 60px 20px; color: #a89a90; }
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
            <h1 class="display-6 fw-bold mb-3">Dicas e Achadinhos da Ely</h1>
            <p class="text-muted" style="max-width: 620px; margin: auto; font-size: 1.1rem;">
                Mais do que uma lista de ofertas: aqui a gente testa, compara e dá a dica de como
                escolher bem em cada categoria, além de garimpar os melhores preços da Amazon
                pro seu Lar e pro Mundo do Bebê. Curadoria feita com carinho por Elyad & Henrique.
            </p>
            <div class="row selo-confianca g-3">
                <div class="col-4 item-selo">
                    <i class="fas fa-magnifying-glass fa-lg mb-2"></i>
                    <div class="titulo-selo">Curadoria manual</div>
                    <div class="desc-selo">Cada oferta é escolhida à mão</div>
                </div>
                <div class="col-4 item-selo">
                    <i class="fas fa-rotate fa-lg mb-2"></i>
                    <div class="titulo-selo">Preços atualizados</div>
                    <div class="desc-selo">Revisados todos os dias</div>
                </div>
                <div class="col-4 item-selo">
                    <i class="fas fa-lightbulb fa-lg mb-2"></i>
                    <div class="titulo-selo">Dicas de verdade</div>
                    <div class="desc-selo">Não é só link, é orientação</div>
                </div>
            </div>
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
             {% if destaques_bebe %}
             <div class="row g-4 mb-5">
                {% for item in destaques_bebe %}
                    {% if item.tipo == 'dica' %}{{ render_dica(item.texto) }}{% else %}{{ render_card(item.dado) }}{% endif %}
                {% endfor %}
             </div>
             {% else %}
             <div class="empty-state mb-5"><i class="fas fa-box-open fa-2x mb-2"></i><p>Novidades chegando em breve por aqui.</p></div>
             {% endif %}

             <h3 class="fw-bold mb-4 mt-5" style="color: var(--cor-texto);">✨ Mais Achadinhos</h3>
             {% if outros_produtos %}
             <div class="row g-4">
                {% for item in outros_produtos %}
                    {% if item.tipo == 'dica' %}{{ render_dica(item.texto) }}{% else %}{{ render_card(item.dado) }}{% endif %}
                {% endfor %}
             </div>
             {% else %}
             <div class="empty-state"><i class="fas fa-box-open fa-2x mb-2"></i><p>Novidades chegando em breve por aqui.</p></div>
             {% endif %}
        {% else %}
             <h2 class="fw-bold mb-3 border-bottom pb-2" style="color: var(--cor-primaria);">{{ titulo_secao }}</h2>
             {% if intro_categoria %}
             <p class="intro-categoria">{{ intro_categoria }}</p>
             {% endif %}
             {% if produtos %}
             <div class="row g-4">
                {% for item in produtos %}
                    {% if item.tipo == 'dica' %}{{ render_dica(item.texto) }}{% else %}{{ render_card(item.dado) }}{% endif %}
                {% endfor %}
             </div>
             {% if total_paginas > 1 %}
             <nav class="mt-5" aria-label="Paginação">
                <ul class="pagination justify-content-center paginacao">
                    {% for n in range(1, total_paginas + 1) %}
                    <li class="page-item {% if n == pagina_atual %}active{% endif %}">
                        <a class="page-link" href="{{ 'cat-' + slug + '.html' if n == 1 else 'cat-' + slug + '-' + n|string + '.html' }}">{{ n }}</a>
                    </li>
                    {% endfor %}
                </ul>
             </nav>
             {% endif %}
             {% else %}
             <div class="empty-state"><i class="fas fa-box-open fa-2x mb-2"></i><p>Nenhuma oferta encontrada nesta categoria no momento.</p></div>
             {% endif %}
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
        {% if p.desconto_pct > 0 %}
        <span class="badge-desconto">-{{ p.desconto_pct }}%</span>
        {% endif %}
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

                <a href="{{ p.link }}" target="_blank" rel="nofollow sponsored noopener" class="btn btn-comprar">
                    Ver na Amazon
                </a>
            </div>
        </div>
    </div>
</div>
{% endmacro %}

{% macro render_dica(texto) %}
<div class="col-12">
    <div class="card-dica">
        <span class="icone-dica">💡</span>
        <div>
            <span class="rotulo-dica">Dica da Ely</span>
            <p>{{ texto }}</p>
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
        preco_atual_f = float(row[1])
        preco_original_f = float(row[2])
        desconto_pct = 0
        if preco_original_f > preco_atual_f > 0:
            desconto_pct = round((1 - (preco_atual_f / preco_original_f)) * 100)

        p = {
            'titulo': row[0],
            'preco_atual': formatar_moeda(row[1]),
            'preco_atual_float': preco_atual_f,
            'preco_original': formatar_moeda(row[2]),
            'preco_original_float': preco_original_f,
            'imagem': row[3],
            'link': row[4],
            'categoria': row[5],
            'nota': row[6],
            'parcelas': row[7],
            'desconto_pct': desconto_pct,
        }
        try: p['estrelas_int'] = int(float(row[6]))
        except: p['estrelas_int'] = 5
        return p
    except Exception as e:
        print(f"Erro ao processar linha: {e}")
        return None

def intercalar_dicas(produtos, categoria):
    """Transforma a lista de produtos numa lista mista de itens {'tipo': 'produto'|'dica'},
    inserindo uma caixinha de dica a cada N produtos. Isso é o que dá o tom editorial ao
    grid, em vez de só uma parede de cards de compra."""
    dicas = CATEGORIA_INFO.get(categoria, {}).get("dicas", [])
    resultado = []
    dica_idx = 0
    for i, p in enumerate(produtos, start=1):
        resultado.append({"tipo": "produto", "dado": p})
        if dicas and i % PRODUTOS_ENTRE_DICAS == 0 and dica_idx < len(dicas):
            resultado.append({"tipo": "dica", "texto": dicas[dica_idx]})
            dica_idx += 1
    return resultado

def gerar_json_ld(produtos, nome_pagina, url_pagina):
    """Gera dados estruturados schema.org (ItemList de Products) para rich snippets no Google."""
    if not produtos:
        return None
    itens = []
    for i, p in enumerate(produtos, start=1):
        itens.append({
            "@type": "ListItem",
            "position": i,
            "item": {
                "@type": "Product",
                "name": p['titulo'],
                "image": p['imagem'],
                "url": p['link'],
                "aggregateRating": {
                    "@type": "AggregateRating",
                    "ratingValue": p['nota'],
                    "bestRating": "5",
                    "reviewCount": "1"
                },
                "offers": {
                    "@type": "Offer",
                    "priceCurrency": "BRL",
                    "price": f"{p['preco_atual_float']:.2f}",
                    "availability": "https://schema.org/InStock",
                    "url": p['link']
                }
            }
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": nome_pagina,
        "url": url_pagina,
        "itemListElement": itens
    }
    return json.dumps(schema, ensure_ascii=False)

def gerar_sitemap(categorias, paginas_por_categoria):
    """Gera o arquivo sitemap.xml, incluindo todas as páginas de cada categoria paginada."""
    print("🗺️  Gerando Sitemap...")
    data_hoje = datetime.now().strftime('%Y-%m-%d')

    urls = [
        (f"{URL_SITE}/", "daily", "1.0"),
        (f"{URL_SITE}/index.html", "daily", "0.8"),
    ]
    for cat in categorias:
        total_paginas = paginas_por_categoria.get(cat['slug'], 1)
        for n in range(1, total_paginas + 1):
            sufixo = "" if n == 1 else f"-{n}"
            urls.append((f"{URL_SITE}/cat-{cat['slug']}{sufixo}.html", "weekly", "0.8"))

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    for loc, freq, prio in urls:
        xml += f"""
   <url>
      <loc>{loc}</loc>
      <lastmod>{data_hoje}</lastmod>
      <changefreq>{freq}</changefreq>
      <priority>{prio}</priority>
   </url>"""
    xml += "\n</urlset>"

    with open(f"{PASTA_SAIDA}/sitemap.xml", "w", encoding="utf-8") as f:
        f.write(xml)

def gerar_robots_txt():
    """Gera o robots.txt liberando a indexação e apontando pro sitemap."""
    conteudo = f"""User-agent: *
Allow: /

Sitemap: {URL_SITE}/sitemap.xml
"""
    with open(f"{PASTA_SAIDA}/robots.txt", "w", encoding="utf-8") as f:
        f.write(conteudo)

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
    cursor.execute("SELECT titulo, preco_atual, preco_original, imagem_url, link_afiliado, categoria, nota, parcelas FROM produtos WHERE categoria = 'Mundo do Bebê' ORDER BY id DESC LIMIT 8")
    destaques_bebe = [p for p in [processar_produto(r) for r in cursor.fetchall()] if p]

    cursor.execute("SELECT titulo, preco_atual, preco_original, imagem_url, link_afiliado, categoria, nota, parcelas FROM produtos WHERE categoria != 'Mundo do Bebê' ORDER BY id DESC LIMIT 40")
    outros_produtos = [p for p in [processar_produto(r) for r in cursor.fetchall()] if p]

    json_ld_home = gerar_json_ld(destaques_bebe + outros_produtos, "Dicas da Ely - Ofertas em Destaque", f"{URL_SITE}/")

    html_home = tpl.render(
        navbar=navbar_html,
        is_home=True,
        json_ld=json_ld_home,
        ga_id=GA_MEASUREMENT_ID,
        titulo_seo="Dicas da Ely | Achadinhos e Ofertas Amazon para Bebê e Casa",
        descricao_seo="Confira nossa seleção de fraldas, itens para enxoval e utilidades domésticas com os melhores preços. Verificado por Elyad & Henrique.",
        imagem_og=f"{URL_SITE}/{ARQUIVO_LOGO}",
        url_atual=f"{URL_SITE}/",
        titulo_pag="Início",
        destaques_bebe=intercalar_dicas(destaques_bebe, "Mundo do Bebê"),
        outros_produtos=intercalar_dicas(outros_produtos, "GERAL"),
        data_atual=data_atual_str
    )
    with open(f"{PASTA_SAIDA}/index.html", "w", encoding="utf-8") as f: f.write(html_home)

    # 5. GERAÇÃO DAS CATEGORIAS (com paginação)
    paginas_por_categoria = {}
    for cat in menu_categorias:
        cursor.execute("SELECT titulo, preco_atual, preco_original, imagem_url, link_afiliado, categoria, nota, parcelas FROM produtos WHERE categoria = ? ORDER BY id DESC", (cat['nome'],))
        prods_cat = [p for p in [processar_produto(r) for r in cursor.fetchall()] if p]

        slug = cat['slug']
        total_paginas = max(1, math.ceil(len(prods_cat) / PRODUTOS_POR_PAGINA))
        paginas_por_categoria[slug] = total_paginas

        for pagina in range(1, total_paginas + 1):
            inicio = (pagina - 1) * PRODUTOS_POR_PAGINA
            fim = inicio + PRODUTOS_POR_PAGINA
            prods_pagina = prods_cat[inicio:fim]

            sufixo_arquivo = "" if pagina == 1 else f"-{pagina}"
            nome_arquivo = f"cat-{slug}{sufixo_arquivo}.html"
            url_pagina = f"{URL_SITE}/{nome_arquivo}"

            json_ld_cat = gerar_json_ld(prods_pagina, f"Ofertas de {cat['nome']}", url_pagina)

            titulo_seo_pag = f"Ofertas de {cat['nome']}" + (f" - Página {pagina}" if pagina > 1 else "") + " | Dicas da Ely"

            html_cat = tpl.render(
                navbar=navbar_html,
                is_home=False,
                json_ld=json_ld_cat,
                ga_id=GA_MEASUREMENT_ID,
                titulo_seo=titulo_seo_pag,
                descricao_seo=f"Encontre as melhores promoções de {cat['nome']} selecionadas a dedo na Amazon.",
                imagem_og=f"{URL_SITE}/{ARQUIVO_LOGO}",
                url_atual=url_pagina,
                titulo_secao=cat['nome'],
                intro_categoria=CATEGORIA_INFO.get(cat['nome'], {}).get("intro"),
                produtos=intercalar_dicas(prods_pagina, cat['nome']),
                slug=slug,
                pagina_atual=pagina,
                total_paginas=total_paginas,
                data_atual=data_atual_str
            )
            with open(f"{PASTA_SAIDA}/{nome_arquivo}", "w", encoding="utf-8") as f: f.write(html_cat)

    # 6. Gerar o Sitemap e o robots.txt
    gerar_sitemap(menu_categorias, paginas_por_categoria)
    gerar_robots_txt()

    conn.close()
    print("✅ SITE GERADO COM SUCESSO!")
    print("   - index.html criado")
    print("   - sitemap.xml e robots.txt criados")
    print("   - Páginas de categoria criadas (com paginação e dados estruturados)")

if __name__ == "__main__":
    main()
