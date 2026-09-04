# Melhorias aplicadas — Dicas da Ely

## 1. Limpeza do repositório
- Removidos `erro_html.html` e `erro_tela.png` que estavam soltos na raiz (vazamento de artefatos de debug).
- `.gitignore` atualizado para cobrir `erro_*.html` (antes só cobria `.png`) e a pasta `debug/`.
- Adicionado `requirements.txt` (selenium, webdriver-manager, beautifulsoup4, jinja2).

## 2. Robustez do robô coletor (robo_coletor.py)
- Logging estruturado em `coleta.log` (console + arquivo) no lugar de `print` solto.
- Retry automático (2 tentativas) quando uma categoria retorna zero itens.
- Artefatos de debug (HTML + screenshot) agora só são salvos quando uma categoria falha,
  numa pasta `debug/` (gitignorada) com rotação automática — mantém só os 5 mais recentes por categoria.
- Erros de parsing por item agora são contados e logados (antes eram engolidos em silêncio),
  então dá pra perceber rápido quando a Amazon muda um seletor.
- User-agent aleatório e pequenas variações de tempo de espera (mais parecido com navegação humana).
- Resumo final no log mostrando quantos itens cada categoria trouxe.

## 3. Visual (gerador_site.py)
- Fonte de destaque (Baloo 2) para títulos, dando mais personalidade à marca.
- Selo de desconto (ex: "-15%") no canto do card quando há preço original.
- Hero da home com gradiente sutil.
- Estado vazio tratado (categoria sem produtos não fica com página em branco).
- Link "Ver na Amazon" agora com `rel="nofollow sponsored noopener"` (recomendado pelo Google para links de afiliado).

## 4. SEO / conversão
- Dados estruturados (schema.org `ItemList` + `Product` + `Offer`) em todas as páginas —
  ajuda o Google a exibir rich snippets com preço e nota.
- Favicon usando a logo.
- `preconnect` para os CDNs (Google Fonts, jsDelivr) — carregamento um pouco mais rápido.
- Paginação de categorias (24 produtos por página) — evita páginas gigantes conforme o catálogo cresce.
- Sitemap.xml agora inclui automaticamente todas as páginas paginadas.

## 5. Rodada seguinte: paralelização + robots.txt
- `robo_coletor.py` agora coleta as 5 categorias **em paralelo** (até 3 ao mesmo tempo,
  ajustável em `MAX_CATEGORIAS_EM_PARALELO`), cada uma com seu próprio Chrome — a coleta
  fica bem mais rápida. O chromedriver é baixado uma única vez antes de abrir os navegadores.
- `banco_de_dados.py` passou a usar `PRAGMA journal_mode=WAL` e `timeout=30` na conexão,
  pra aguentar várias threads gravando no SQLite ao mesmo tempo sem erro de "database is locked".
- Novo `site_publico/robots.txt`, liberando indexação e apontando pro sitemap.

## 6. Google Analytics 4
- Propriedade GA4 "Dicas da Ely" criada, ID `G-JDYT3SLVZJ`.
- Tag do gtag.js integrada direto no `HEAD_COMUM` do `gerador_site.py` (constante `GA_MEASUREMENT_ID`),
  então toda página gerada (home e categorias) já sai com o rastreamento ativo.
- Leva até 48h pros primeiros dados aparecerem no relatório em tempo real do Analytics.

## 7. Layout com cara de site de dicas (não só links)
- Hero da home reescrito com uma proposta editorial clara ("mais do que uma lista de ofertas")
  e uma faixa de confiança com 3 selos: curadoria manual, preços atualizados, dicas de verdade.
- Cada página de categoria ganhou um parágrafo de introdução (`intro_categoria`) explicando o
  que considerar na hora de escolher naquele tipo de produto.
- Caixinhas "💡 Dica da Ely" intercaladas no meio do grid de produtos (a cada 8 itens), com
  orientações genuínas de compra por categoria — não é resenha inventada de produto específico,
  é o tipo de dica que qualquer comprador deveria saber antes de escolher.
- Conteúdo das dicas fica centralizado em `CATEGORIA_INFO` no `gerador_site.py`, fácil de editar
  ou ampliar (é só editar o dicionário e rodar o gerador de novo).

## O que NÃO foi mexido
- Estrutura do banco de dados (banco_de_dados.py) — mantida como estava, só validada.
- Workflow do GitHub Actions — já estava correto (só gera e publica; a coleta continua rodando local via Task Scheduler).
