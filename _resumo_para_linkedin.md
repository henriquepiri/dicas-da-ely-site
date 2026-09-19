# Contexto para atualizar o LinkedIn — Dicas da Ely

Site: dicasdaely.com.br. Amazon-afiliado, nicho bebê/casa/cozinha/tecnologia/cuidados
pessoais. Rodado por Henrique (planejamento de produção industrial na Steelmast) e sua
esposa Elyad, pais de uma criança pequena. Site 100% estático (GitHub Pages), gerado por
scripts Python que Henrique escreveu.

## O que mudou nesta sessão (2026-09-08 a 2026-09-10)

**Qualidade dos dados**
- Corrigido bug que publicava produto com título vazio/genérico ("Genérico", "Era Uma
  Vez") em vez do nome real — 13 ofertas já no ar tinham esse defeito.
- Corrigido erro de tradução automática em títulos de anunciantes estrangeiros (ex:
  "Adaptador durante zigbee" → "Adaptador zigbee").
- Home deixou de mostrar produto só por ordem de chegada: agora exige nota mínima 4,3 na
  Amazon, e o selo do site ("Curadoria manual") virou "Seleção por qualidade" pra bater
  com a regra real.
- Removido produto sensível (item de sono infantil) do catálogo por decisão editorial,
  com trava permanente pra não voltar sozinho numa coleta futura.
- Corrigido bug em que a caixinha "Dica da Ely" sumia em categoria com poucos produtos.

**Voz e texto**
- Removido travessão (—) de todo o texto do site (guias, categorias, rodapé, páginas
  institucionais) — é um tique reconhecível de texto gerado por IA, e o diferencial do
  site é soar como pais de verdade escrevendo, não como conteúdo genérico.
- Criado um assistente (usa API da OpenAI) que ajuda a revisar a fluidez de um guia ou
  rascunhar um guia novo a partir de tópicos reais que Henrique/Elyad fornecem — nunca
  inventa experiência ou produto, só lapida o que é fornecido.

**SEO**
- Adicionado H1 nas páginas de categoria (não tinham nenhum).
- Meta tags Twitter Card e og:site_name/locale.
- Sitemap passou a usar a data real de cada página (guia usa a data de publicação,
  página institucional usa a data de revisão) em vez da mesma data em tudo.
- Nova página `/guias.html`: lista cronológica de todos os guias (antes só dava pra
  achar pela home ou navegando categoria por categoria).
- Links de contexto dentro do texto dos guias, ligando guias relacionados entre si.
- Cada guia ganhou uma **capa própria gerada por código** (1200×630, ícone do assunto +
  cores/fonte do site) — usada como imagem de compartilhamento social (og:image) e no
  topo do próprio artigo. Antes todos os guias compartilhavam a mesma logo genérica.
- Acessibilidade: aria-label no botão de compra, contraste do preço riscado corrigido.

**Infraestrutura (mudança grande)**
- O DNS estava na Netlify, que mudou pra cobrança por crédito e começou a bloquear
  silenciosamente a edição/entrega dos registros — o site ficou fora do ar sem aviso
  claro. Migrado o DNS inteiro pra Cloudflare (gratuito, sem essa trava).
- Criado e-mail `contato@dicasdaely.com.br` (redirecionamento gratuito via ImprovMX).
- Robô de coleta agora roda em modo headless — a tarefa agendada diária estava falhando
  silenciosamente quando o PC ficava com a tela travada no horário.

**Newsletter (novo)**
- Formulário de cadastro no rodapé do site (Brevo, plano grátis), com a cara do site em
  vez do estilo padrão da ferramenta.
- Domínio autenticado (DKIM/DMARC) pra não cair em spam.
- E-mail automático disparado pros inscritos toda vez que um guia novo é publicado
  (não a cada atualização diária de preço) — testado de ponta a ponta, com link de
  descadastro funcionando.

## Estado atual
7 guias publicados, ~108 ofertas no ar, atualização automática diária (robô +
regeneração do site), newsletter ativa. Repositório público:
github.com/henriquepiri/dicas-da-ely-site — todo trabalho recente passou por Pull
Request (branch + revisão), não commit direto.

## Pendências conhecidas
- Revisão jurídica da política de privacidade, agora que o site coleta e-mail
  diretamente (formulário de newsletter) — hoje é só um rascunho em linguagem comum.
- Elyad ainda precisa revisar o tom/fatos dos textos dos guias.
- Publicar um guia novo por semana é a meta; temas que faltam: primeiro banho, bolsa de
  maternidade, voltar a trabalhar, passeio com bebê, introdução alimentar.
