import sqlite3
import os
import shutil
import re
import json
import math
from datetime import datetime
from jinja2 import Template
from guias import GUIAS
from paginas import PAGINAS

# --- CONFIGURAÇÕES ---
PASTA_SAIDA = "docs"  # GitHub Pages só publica da raiz ou de uma pasta chamada "docs"
NOME_BANCO = "estoque_ofertas.db"
ARQUIVO_LOGO = "logo_dicas.png"
URL_SITE = "https://dicasdaely.com.br"
DOMINIO_CUSTOMIZADO = "dicasdaely.com.br"  # vira o arquivo CNAME do GitHub Pages
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

        .navbar { background: white; border-bottom: 1px solid var(--cor-card-border); box-shadow: none; padding: 0; }
        .navbar > .container { max-width: 1140px; }
        .logo-img { height: 46px; width: auto; display: block; }
        .navbar-brand { padding: 14px 0; margin-right: 40px; }
        .nav-link { color: var(--cor-texto) !important; font-weight: 700; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.4px; padding: 22px 0 !important; margin: 0 14px; border-bottom: 2px solid transparent; }
        .nav-link:hover { color: var(--cor-destaque) !important; border-bottom-color: var(--cor-destaque); }
        @media (max-width: 991px) {
            .nav-link { padding: 10px 0 !important; margin: 0; border-bottom: none; }
            .navbar-brand { margin-right: 0; }
        }

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

        /* --- GUIAS (conteúdo editorial) --- */
        .guia-destaque { background: white; border: 1px solid var(--cor-card-border); border-radius: 16px; overflow: hidden; margin-bottom: 40px; transition: 0.25s; }
        .guia-destaque:hover { box-shadow: 0 16px 32px rgba(140, 94, 74, 0.14); }
        .guia-destaque .corpo { padding: 32px; }
        .guia-destaque .etiqueta { display: inline-block; background: var(--cor-destaque); color: white; font-size: 0.7rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.6px; padding: 5px 12px; border-radius: 30px; margin-bottom: 14px; }
        .guia-destaque h2 { font-size: 1.9rem; color: var(--cor-primaria); margin-bottom: 12px; line-height: 1.2; }
        .guia-destaque p { color: #8a7a70; font-size: 1.05rem; line-height: 1.6; margin-bottom: 18px; }

        .card-guia { display: block; background: white; border: 1px solid var(--cor-card-border); border-radius: 14px; padding: 22px; height: 100%; text-decoration: none; transition: 0.25s; }
        .card-guia:hover { transform: translateY(-5px); box-shadow: 0 12px 24px rgba(140, 94, 74, 0.14); border-color: var(--cor-primaria); }
        .card-guia .cat { font-size: 0.68rem; color: var(--cor-primaria); font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; }
        .card-guia h3 { font-size: 1.15rem; color: var(--cor-texto); margin: 8px 0 10px; line-height: 1.3; }
        .card-guia p { font-size: 0.88rem; color: #9a8a80; line-height: 1.5; margin: 0; }
        .card-guia .ler { color: var(--cor-destaque); font-weight: 800; font-size: 0.85rem; margin-top: 14px; display: block; }

        .link-simples { color: var(--cor-destaque); font-weight: 800; text-decoration: none; }
        .link-simples:hover { text-decoration: underline; }

        /* --- PÁGINA DO GUIA --- */
        .artigo { max-width: 720px; margin: 0 auto; }
        .artigo h1 { font-size: 2.3rem; color: var(--cor-primaria); line-height: 1.15; margin-bottom: 14px; }
        .artigo .meta { color: #a89a90; font-size: 0.85rem; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid var(--cor-card-border); }
        .artigo h2 { font-size: 1.45rem; color: var(--cor-texto); margin: 34px 0 14px; }
        .artigo p { font-size: 1.08rem; line-height: 1.75; margin-bottom: 18px; color: #6b5546; }
        .artigo ul { margin-bottom: 20px; }
        .artigo li { font-size: 1.05rem; line-height: 1.7; margin-bottom: 10px; color: #6b5546; }
        .artigo strong { color: var(--cor-texto); }

        .caixa-autor { background: #fff7f0; border-radius: 14px; padding: 24px; margin: 40px 0; display: flex; gap: 18px; align-items: center; }
        .caixa-autor .iniciais { width: 56px; height: 56px; border-radius: 50%; background: var(--cor-primaria); color: white; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.1rem; flex-shrink: 0; }
        .caixa-autor p { margin: 0; font-size: 0.92rem; color: #8a7a70; line-height: 1.55; }

        .aviso-afiliado { background: #f7f3ef; border-radius: 10px; padding: 14px 18px; font-size: 0.82rem; color: #9a8a80; margin-bottom: 32px; line-height: 1.5; }

        .rodape-link { color: var(--cor-primaria); font-weight: 700; text-decoration: none; font-size: 0.85rem; }
        .rodape-link:hover { color: var(--cor-destaque); text-decoration: underline; }
        .rodape-sep { color: #d8ccc4; margin: 0 8px; }

        /* --- AJUSTES PARA CELULAR --- */
        @media (max-width: 767px) {
            .hero { padding: 30px 0; margin-bottom: 26px; }
            .hero h1 { font-size: 1.75rem; }
            .hero p { font-size: 0.98rem !important; }
            .selo-confianca { margin-top: 22px; }
            .selo-confianca .item-selo .titulo-selo { font-size: 0.75rem; }
            .selo-confianca .item-selo .desc-selo { font-size: 0.7rem; }

            .guia-destaque .corpo { padding: 22px; }
            .guia-destaque h2 { font-size: 1.4rem; }
            .guia-destaque p { font-size: 0.95rem; }

            .artigo h1 { font-size: 1.65rem; }
            .artigo h2 { font-size: 1.2rem; margin-top: 26px; }
            .artigo p, .artigo li { font-size: 1rem; }

            .caixa-autor { flex-direction: column; text-align: center; gap: 12px; padding: 20px; }

            /* cards em duas colunas no celular: imagem e texto menores para caber */
            .img-wrap { height: 140px; padding: 10px; }
            /* 3 linhas no celular: com a coluna estreita, 2 linhas cortam o nome cedo
               demais e o visitante não consegue saber o que é o produto */
            .titulo-prod { font-size: 0.85rem; -webkit-line-clamp: 3; }
            .preco-atual { font-size: 1.2rem; }
            .parcelamento { font-size: 0.72rem; margin-bottom: 10px; }
            .categoria-tag { font-size: 0.6rem; }
            .btn-comprar { font-size: 0.8rem; padding: 8px; }
            .card-body { padding: 12px; }
            .card-dica { padding: 16px; }
        }

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
                {% endfor %}            </ul>
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
             {% if guia_destaque %}
             <div class="guia-destaque">
                <div class="corpo">
                    <span class="etiqueta">Guia da semana</span>
                    <h2>{{ guia_destaque.titulo }}</h2>
                    <p>{{ guia_destaque.resumo }}</p>
                    <a href="guia-{{ guia_destaque.slug }}.html" class="btn btn-comprar" style="width: auto; padding: 10px 28px; display: inline-block;">Ler o guia completo</a>
                </div>
             </div>
             {% endif %}

             {% if outros_guias %}
             <div class="d-flex align-items-center justify-content-between mb-4 mt-5 pb-2 border-bottom border-2" style="border-color: #f0e6e0 !important;">
                <h3 class="fw-bold m-0" style="color: var(--cor-texto);">Nossos guias</h3>
             </div>
             <div class="row g-4 mb-5">
                {% for g in outros_guias %}
                <div class="col-12 col-md-6 col-lg-4">
                    <a href="guia-{{ g.slug }}.html" class="card-guia">
                        <span class="cat">{{ g.categoria }}</span>
                        <h3>{{ g.titulo }}</h3>
                        <p>{{ g.resumo }}</p>
                        <span class="ler">Ler o guia &rarr;</span>
                    </a>
                </div>
                {% endfor %}
             </div>
             {% endif %}

             <div class="caixa-autor">
                <div class="iniciais">EH</div>
                <p><strong style="color: var(--cor-texto);">Elyad &amp; Henrique.</strong>
                Somos pais de uma criança pequena e escrevemos aqui o que aprendemos na
                prática — o que funcionou, o que foi dinheiro jogado fora e o que a gente
                queria ter sabido antes.</p>
             </div>

             <div class="d-flex align-items-center justify-content-between mb-4 mt-5 pb-2 border-bottom border-2" style="border-color: #f0e6e0 !important;">
                <h3 class="fw-bold m-0" style="color: var(--cor-texto);">Ofertas de hoje</h3>
                <span class="text-muted small">Atualizado em {{ data_atual }}</span>
             </div>
             {% if destaques_bebe %}
             <div class="row g-4 mb-5">
                {% for item in destaques_bebe %}
                    {% if item.tipo == 'dica' %}{{ render_dica(item.texto) }}{% else %}{{ render_card(item.dado) }}{% endif %}
                {% endfor %}
             </div>
             {% endif %}
             {% if outros_produtos %}
             <div class="row g-4">
                {% for item in outros_produtos %}
                    {% if item.tipo == 'dica' %}{{ render_dica(item.texto) }}{% else %}{{ render_card(item.dado) }}{% endif %}
                {% endfor %}
             </div>
             {% endif %}
             {% if not destaques_bebe and not outros_produtos %}
             <div class="empty-state"><i class="fas fa-box-open fa-2x mb-2"></i><p>Novidades chegando em breve por aqui.</p></div>
             {% endif %}
        {% else %}
             <h2 class="fw-bold mb-3 border-bottom pb-2" style="color: var(--cor-primaria);">{{ titulo_secao }}</h2>
             {% if intro_categoria %}
             <p class="intro-categoria">{{ intro_categoria }}</p>
             {% endif %}
             {% if guias_da_categoria %}
             <div class="row g-3 mb-5">
                {% for g in guias_da_categoria %}
                <div class="col-12 col-md-6">
                    <a href="guia-{{ g.slug }}.html" class="card-guia">
                        <span class="cat">Guia</span>
                        <h3>{{ g.titulo }}</h3>
                        <p>{{ g.resumo }}</p>
                        <span class="ler">Ler o guia &rarr;</span>
                    </a>
                </div>
                {% endfor %}
             </div>
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

    {{ rodape }}

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

TEMPLATE_GUIA = """
<!DOCTYPE html>
<html lang="pt-br">
{{ head }}
<body>
    {{ navbar }}

    <div class="container py-5">
        <article class="artigo">
            <a href="index.html" class="link-simples" style="font-size: 0.85rem;">&larr; Voltar para a home</a>
            <h1 class="mt-3">{{ guia.titulo }}</h1>
            <div class="meta">
                {{ guia.categoria }} &middot; Publicado em {{ guia.data_br }} &middot; por Elyad &amp; Henrique
            </div>

            <div class="aviso-afiliado">
                Este guia tem links de afiliado da Amazon. Se você comprar por um deles, a gente
                recebe uma pequena comissão sem custo extra pra você — é o que mantém o site no ar.
                As recomendações são as mesmas que daríamos sem isso.
            </div>

            {{ guia.conteudo }}

            <div class="caixa-autor">
                <div class="iniciais">EH</div>
                <p><strong style="color: var(--cor-texto);">Elyad &amp; Henrique.</strong>
                Somos pais de uma criança pequena e escrevemos aqui o que aprendemos na prática.
                Se tiver dúvida ou quiser sugerir um tema, é só falar com a gente.</p>
            </div>

            {% if produtos_relacionados %}
            <h2 class="mt-5 mb-4" style="color: var(--cor-primaria);">Ofertas de {{ guia.categoria }}</h2>
            <div class="row g-4">
                {% for p in produtos_relacionados %}
                    {{ render_card(p) }}
                {% endfor %}
            </div>
            <p class="mt-4">
                <a href="cat-{{ slug_categoria }}.html" class="link-simples">Ver todas as ofertas de {{ guia.categoria }} &rarr;</a>
            </p>
            {% endif %}

            {% if outros_guias %}
            <h2 class="mt-5 mb-4" style="color: var(--cor-primaria);">Leia também</h2>
            <div class="row g-3">
                {% for g in outros_guias %}
                <div class="col-12 col-md-6">
                    <a href="guia-{{ g.slug }}.html" class="card-guia">
                        <span class="cat">{{ g.categoria }}</span>
                        <h3>{{ g.titulo }}</h3>
                        <p>{{ g.resumo }}</p>
                    </a>
                </div>
                {% endfor %}
            </div>
            {% endif %}
        </article>
    </div>

    {{ rodape }}

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

TEMPLATE_PAGINA = """
<!DOCTYPE html>
<html lang="pt-br">
{{ head }}
<body>
    {{ navbar }}
    <div class="container py-5">
        <article class="artigo">
            <a href="index.html" class="link-simples" style="font-size: 0.85rem;">&larr; Voltar para a home</a>
            <h1 class="mt-3">{{ pagina.titulo }}</h1>
            <div class="meta">Atualizado em {{ pagina.atualizado_br }}</div>
            {{ pagina.conteudo }}
        </article>
    </div>
    {{ rodape }}
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

RODAPE = """
    <footer class="bg-white py-4 mt-5 border-top text-center small">
        <div class="container">
            <img src="logo_dicas.png" alt="Dicas da Ely" style="height: 34px; opacity: 0.55; margin-bottom: 12px;">
            <p class="mb-2">
                <a href="sobre.html" class="rodape-link">Sobre</a>
                <span class="rodape-sep">&middot;</span>
                <a href="politica-de-privacidade.html" class="rodape-link">Privacidade</a>
                <span class="rodape-sep">&middot;</span>
                <a href="termos-de-uso.html" class="rodape-link">Termos de uso</a>
            </p>
            <p class="mb-1 fw-bold text-muted">© 2026 Dicas da Ely</p>
            <small class="text-muted d-block" style="max-width: 520px; margin: 0 auto; line-height: 1.5;">
                Participante do Programa de Associados da Amazon. Recebemos comissão por compras
                qualificadas, sem custo extra para você. Preços podem mudar — confira sempre na Amazon.
            </small>
            <p class="mt-2 text-muted" style="font-size: 0.75rem">Ofertas atualizadas em {{ data_atual }}</p>
        </div>
    </footer>
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

def preparar_guias():
    """Ordena os guias por data (mais recente primeiro) e formata a data para exibição.
    Separa o guia em destaque dos demais."""
    guias = []
    for g in GUIAS:
        g2 = dict(g)
        try:
            g2['data_br'] = datetime.strptime(g['data'], '%Y-%m-%d').strftime('%d/%m/%Y')
        except Exception:
            g2['data_br'] = g.get('data', '')
        guias.append(g2)

    guias.sort(key=lambda x: x.get('data', ''), reverse=True)

    destaque = next((g for g in guias if g.get('destaque')), guias[0] if guias else None)
    outros = [g for g in guias if g is not destaque]
    return guias, destaque, outros

def gerar_json_ld_artigo(guia, url_pagina):
    """Dados estruturados do tipo Article — ajuda o Google a entender que é conteúdo
    editorial, não uma página de produto."""
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": guia['titulo'],
        "description": guia['resumo'],
        "datePublished": guia['data'],
        "author": {"@type": "Person", "name": "Elyad & Henrique"},
        "publisher": {
            "@type": "Organization",
            "name": "Dicas da Ely",
            "logo": {"@type": "ImageObject", "url": f"{URL_SITE}/{ARQUIVO_LOGO}"}
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": url_pagina}
    }
    return json.dumps(schema, ensure_ascii=False)

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

def gerar_sitemap(categorias, paginas_por_categoria, guias=None):
    """Gera o arquivo sitemap.xml, incluindo todas as páginas de cada categoria paginada
    e as páginas de guia."""
    print("🗺️  Gerando Sitemap...")
    data_hoje = datetime.now().strftime('%Y-%m-%d')

    urls = [
        (f"{URL_SITE}/", "daily", "1.0"),
        (f"{URL_SITE}/index.html", "daily", "0.8"),
    ]
    # Guias têm prioridade alta: é o conteúdo original do site
    for g in (guias or []):
        urls.append((f"{URL_SITE}/guia-{g['slug']}.html", "monthly", "0.9"))

    # Páginas institucionais: mudam pouco e têm prioridade baixa, mas precisam ser
    # indexáveis (a de privacidade é exigência prática de LGPD e do programa de afiliados)
    for pag in PAGINAS:
        urls.append((f"{URL_SITE}/{pag['slug']}.html", "yearly", "0.3"))

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

def gerar_arquivos_github_pages():
    """Recria os arquivos que o GitHub Pages precisa. Isso roda a cada geração porque
    o main() apaga a pasta de saída inteira antes de regerar — sem isso, o domínio
    customizado se perderia a cada atualização do site.
      - CNAME: diz ao GitHub Pages qual domínio serve este site
      - .nojekyll: desliga o processamento Jekyll (desnecessário aqui e mais lento)"""
    with open(f"{PASTA_SAIDA}/CNAME", "w", encoding="utf-8") as f:
        f.write(DOMINIO_CUSTOMIZADO + "\n")
    with open(f"{PASTA_SAIDA}/.nojekyll", "w", encoding="utf-8") as f:
        f.write("")

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
    tpl_guia = Template(MACRO_CARD + TEMPLATE_GUIA.replace("{{ head }}", HEAD_COMUM))
    tpl_pagina = Template(TEMPLATE_PAGINA.replace("{{ head }}", HEAD_COMUM))
    navbar_html = Template(NAVBAR).render(categorias=menu_categorias)
    data_atual_str = datetime.now().strftime('%d/%m/%Y')
    rodape_html = Template(RODAPE).render(data_atual=data_atual_str)

    # 3b. Preparar os guias (conteúdo editorial vindo de guias.py)
    todos_guias, guia_destaque, outros_guias = preparar_guias()

    # 4. GERAÇÃO DA HOME (index.html)
    cursor.execute("SELECT titulo, preco_atual, preco_original, imagem_url, link_afiliado, categoria, nota, parcelas FROM produtos WHERE categoria = 'Mundo do Bebê' ORDER BY id DESC LIMIT 8")
    destaques_bebe = [p for p in [processar_produto(r) for r in cursor.fetchall()] if p]

    cursor.execute("SELECT titulo, preco_atual, preco_original, imagem_url, link_afiliado, categoria, nota, parcelas FROM produtos WHERE categoria != 'Mundo do Bebê' ORDER BY id DESC LIMIT 40")
    outros_produtos = [p for p in [processar_produto(r) for r in cursor.fetchall()] if p]

    json_ld_home = gerar_json_ld(destaques_bebe + outros_produtos, "Dicas da Ely - Ofertas em Destaque", f"{URL_SITE}/")

    html_home = tpl.render(
        navbar=navbar_html,
        rodape=rodape_html,
        is_home=True,
        json_ld=json_ld_home,
        ga_id=GA_MEASUREMENT_ID,
        titulo_seo="Dicas da Ely | Guias e Achadinhos para Bebê, Casa e Cozinha",
        descricao_seo="Guias práticos escritos por quem testou: enxoval de bebê, brinquedo seguro, organização de cozinha. Mais ofertas selecionadas da Amazon, atualizadas todo dia.",
        imagem_og=f"{URL_SITE}/{ARQUIVO_LOGO}",
        url_atual=f"{URL_SITE}/",
        titulo_pag="Início",
        guia_destaque=guia_destaque,
        outros_guias=outros_guias,
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
                rodape=rodape_html,
                is_home=False,
                json_ld=json_ld_cat,
                ga_id=GA_MEASUREMENT_ID,
                titulo_seo=titulo_seo_pag,
                descricao_seo=f"Encontre as melhores promoções de {cat['nome']} selecionadas a dedo na Amazon.",
                imagem_og=f"{URL_SITE}/{ARQUIVO_LOGO}",
                url_atual=url_pagina,
                titulo_secao=cat['nome'],
                intro_categoria=CATEGORIA_INFO.get(cat['nome'], {}).get("intro"),
                guias_da_categoria=[g for g in todos_guias if g['categoria'] == cat['nome']] if pagina == 1 else [],
                produtos=intercalar_dicas(prods_pagina, cat['nome']),
                slug=slug,
                pagina_atual=pagina,
                total_paginas=total_paginas,
                data_atual=data_atual_str
            )
            with open(f"{PASTA_SAIDA}/{nome_arquivo}", "w", encoding="utf-8") as f: f.write(html_cat)

    # 5b. GERAÇÃO DAS PÁGINAS DE GUIA
    for guia in todos_guias:
        nome_arquivo = f"guia-{guia['slug']}.html"
        url_pagina = f"{URL_SITE}/{nome_arquivo}"
        slug_cat = criar_slug(guia['categoria'])

        # Puxa alguns produtos da mesma categoria do guia, pra fechar o ciclo
        # entre o conteúdo e a oferta
        cursor.execute(
            "SELECT titulo, preco_atual, preco_original, imagem_url, link_afiliado, categoria, nota, parcelas "
            "FROM produtos WHERE categoria = ? ORDER BY id DESC LIMIT 4",
            (guia['categoria'],)
        )
        relacionados = [p for p in [processar_produto(r) for r in cursor.fetchall()] if p]

        html_guia = tpl_guia.render(
            navbar=navbar_html,
            rodape=rodape_html,
            ga_id=GA_MEASUREMENT_ID,
            json_ld=gerar_json_ld_artigo(guia, url_pagina),
            titulo_seo=f"{guia['titulo']} | Dicas da Ely",
            descricao_seo=guia['resumo'],
            imagem_og=f"{URL_SITE}/{ARQUIVO_LOGO}",
            url_atual=url_pagina,
            guia=guia,
            slug_categoria=slug_cat,
            produtos_relacionados=relacionados,
            outros_guias=[g for g in todos_guias if g['slug'] != guia['slug']][:2],
            data_atual=data_atual_str
        )
        with open(f"{PASTA_SAIDA}/{nome_arquivo}", "w", encoding="utf-8") as f:
            f.write(html_guia)

    # 5c. GERAÇÃO DAS PÁGINAS INSTITUCIONAIS (sobre, privacidade, termos)
    for pag in PAGINAS:
        p2 = dict(pag)
        try:
            p2['atualizado_br'] = datetime.strptime(pag['atualizado'], '%Y-%m-%d').strftime('%d/%m/%Y')
        except Exception:
            p2['atualizado_br'] = pag.get('atualizado', '')

        nome_arquivo = f"{pag['slug']}.html"
        html_pag = tpl_pagina.render(
            navbar=navbar_html,
            rodape=rodape_html,
            ga_id=GA_MEASUREMENT_ID,
            json_ld=None,
            titulo_seo=f"{pag['titulo']} | Dicas da Ely",
            descricao_seo=pag['resumo'],
            imagem_og=f"{URL_SITE}/{ARQUIVO_LOGO}",
            url_atual=f"{URL_SITE}/{nome_arquivo}",
            pagina=p2,
            data_atual=data_atual_str
        )
        with open(f"{PASTA_SAIDA}/{nome_arquivo}", "w", encoding="utf-8") as f:
            f.write(html_pag)

    # 6. Gerar o Sitemap, robots.txt e arquivos do GitHub Pages
    gerar_sitemap(menu_categorias, paginas_por_categoria, todos_guias)
    gerar_robots_txt()
    gerar_arquivos_github_pages()

    conn.close()
    print("✅ SITE GERADO COM SUCESSO!")
    print(f"   - Pasta de saída: {PASTA_SAIDA}/")
    print(f"   - {len(todos_guias)} páginas de guia criadas")
    print(f"   - {len(PAGINAS)} páginas institucionais criadas")
    print("   - index.html criado")
    print("   - sitemap.xml, robots.txt, CNAME e .nojekyll criados")
    print("   - Páginas de categoria criadas (com paginação e dados estruturados)")

if __name__ == "__main__":
    main()
