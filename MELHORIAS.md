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

## 8. Migração Netlify -> GitHub Pages
Motivo: os builds da Netlify pausaram por falta de créditos no plano free. O site é 100%
estático (o HTML já vai pronto pro repositório), então pagar minutos de build era desperdício.
O GitHub Pages serve arquivos commitados direto, sem build e sem limite em repo público.

- `PASTA_SAIDA` mudou de `site_publico` para `docs` (o GitHub Pages só publica da raiz ou de `docs/`).
- Nova função `gerar_arquivos_github_pages()` recria a cada execução:
  - `CNAME` com o domínio customizado — essencial, porque o main() apaga a pasta de saída
    inteira antes de regerar, e sem isso o domínio se perderia a cada atualização.
  - `.nojekyll` para desligar o processamento Jekyll (desnecessário e mais lento).
- Workflow do Actions ajustado para commitar `docs/` em vez de `site_publico/`.

## 9. Guias: o site vira conteúdo, não só vitrine
Mudança de estrutura, não de enfeite: o texto passou a ser o produto principal e a oferta
virou consequência.

- Novo arquivo `guias.py` com o CONTEÚDO dos guias, separado da lógica. Para escrever ou
  editar um guia, mexe-se só nesse arquivo — o gerador_site.py nunca precisa ser tocado.
- Cada guia vira uma página própria (`guia-<slug>.html`) com layout de artigo:
  tipografia de leitura, largura confortável, caixa de autoria e aviso de afiliado no topo.
- Home reordenada: guia em destaque -> grade de guias -> quem escreve -> ofertas do dia.
  Os produtos continuam lá, mas embaixo, como apoio.
- Páginas de categoria mostram os guias daquele tema antes da lista de produtos.
- Cada guia puxa 4 produtos da sua categoria no final, fechando o ciclo conteúdo -> oferta.
- Dados estruturados `Article` (schema.org) nas páginas de guia — sinaliza ao Google que é
  conteúdo editorial, não página de produto. Guias entram no sitemap com prioridade 0.9.

## 10. Cabeçalho e logo
- A logo era um PNG 1024x1024 totalmente opaco, com fundo creme (#FDF6F0) e uma margem
  vazia gigante — por isso aparecia como um "quadrado colado" sobre a barra branca.
  Removido o fundo (flood fill a partir das bordas, para não comer o bege da prancheta
  do desenho), recortada para o conteúdo e redimensionada. De 219KB para ~67KB.
  Ressalva: os miolos fechados das letras seguem cor creme; imperceptível sobre fundo
  claro, mas a logo não deve ser usada sobre fundo escuro.
- Barra mais baixa e enxuta, sombra trocada por hairline; menu com itens menores e mais
  próximos, sublinhado no hover; container limitado a 1140px para a logo não ficar
  isolada em telas largas.

## 11. Correção: preços vinham sem centavos (bug)
Sintoma: todo preço no site aparecia redondo (R$ 369,00) enquanto na Amazon tinha
centavos. 100% dos 60 produtos do banco estavam assim.

Causa: o scraper lia a classe `a-price-whole`, que contém APENAS a parte inteira do
preço ("89,"). Os centavos ficam numa classe separada, `a-price-fraction`. O
`.replace(",", ".")` transformava "89," em "89." -> 89.0, descartando os centavos.

Correção: nova função `extrair_preco_atual()` que lê o span `a-offscreen` dentro de
`a-price` (onde a Amazon coloca o preço completo, "R$ 89,90"), com `a-price-whole` +
`a-price-fraction` como reserva caso o layout mude. Adicionado `_texto_para_float()`
para centralizar a conversão e tratar separador de milhar (R$ 1.299,99 -> 1299.99).

Os preços antigos do banco só são corrigidos na próxima coleta.

## 12. Páginas institucionais e ajustes de celular
- Novo `paginas.py` (mesma ideia do guias.py: só conteúdo, sem lógica) com três páginas:
  política de privacidade, termos de uso e sobre. Geradas como `<slug>.html`.
  A de privacidade era uma lacuna concreta: o site usa Google Analytics (cookies), o que
  pela LGPD exige política acessível, e o Programa de Associados da Amazon também espera isso.
  ATENÇÃO: os textos são um ponto de partida em linguagem comum, não peça jurídica revisada.
- Rodapé unificado numa constante `RODAPE` (antes estava duplicado em dois templates) com
  links para as três páginas e o aviso de afiliado mais explícito.
- Bloco `@media (max-width: 767px)` ajustando hero, cards de produto, tipografia dos guias
  e a caixa de autoria para telas pequenas — onde vem a maior parte do tráfego.
- Páginas institucionais incluídas no sitemap com prioridade baixa (0.3).

## 13. Nova tag de afiliado + bug do link que não atualizava
- `TAG_AFILIADO` mudou de `elyad96-20` para `dicasdaely05-20`.
- BUG encontrado ao fazer essa troca: o `ON CONFLICT(asin) DO UPDATE` do salvar_oferta
  NÃO atualizava o campo `link_afiliado`. Como o link carrega a tag, trocar a tag no
  scraper só valeria para ASINs novos — os produtos já existentes continuariam
  apontando para a tag antiga indefinidamente, mandando comissão para a conta errada.
  Corrigido: o upsert agora atualiza também `link_afiliado`, `titulo` e `imagem_url`
  (estes dois também ficavam congelados na primeira coleta).
- Para os links antigos serem regravados, basta rodar o robo_coletor.py uma vez.

## 14. Links de afiliado no formato canônico
Descoberto ao testar o Verificador de Links da Central de Associados: ele REJEITA
("Insira uma URL válida") as URLs que o site vinha gerando, e aceita a versão curta.

Causa: o scraper usava o href exatamente como aparece na página de busca, carregado de
parâmetros de sessão (dib=, qid=, sr=, ref=, ufe=, th=). Funcionam para comissão, mas
expiram, são enormes, o `th=1` pode fixar uma variação indesejada do produto, e não
passam na ferramenta oficial de verificação.

- Nova função `montar_link_afiliado()` no robo_coletor.py, que monta a URL a partir do
  ASIN já extraído: `https://www.amazon.com.br/dp/<ASIN>?tag=<TAG>`.
  Esse formato foi testado no Verificador e retornou "Bem-sucedido: o link está marcado
  como uma tag válida".
- `limpar_links.py`: script de execução única para converter os links já gravados.
  Depois de rodar, pode ser apagado — o coletor já grava no formato certo.

## 15. Validade das ofertas, mais guias e material de revisão
- `DIAS_VALIDADE_OFERTA` (10 dias): ofertas sem revisão há mais tempo somem do site.
  Motivo: o banco só cresce e cada coleta revisita apenas parte dos produtos, então item
  antigo ficava no ar com preço defasado — o visitante clicava esperando um valor e
  encontrava outro na Amazon.
- Proteção `MIN_PRODUTOS_PARA_FILTRAR` (20): se o corte deixar menos que isso, ele é
  ignorado e o gerador avisa no console. Evita que uma coleta quebrada esvazie o site
  silenciosamente.
- Dois guias novos: fralda (tamanho e quantidade) e quarto de bebê pequeno. Total: 7.
- `COMO-EDITAR-GUIAS.md`: instruções em linguagem comum para Henrique e Elyad revisarem
  os textos, criarem guias novos e publicarem, sem precisar entender o gerador.
