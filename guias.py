# -*- coding: utf-8 -*-
"""
CONTEÚDO DOS GUIAS — Dicas da Ely

Este arquivo guarda só o TEXTO dos guias. Para editar um guia, mexa aqui;
nunca é preciso tocar no gerador_site.py.

Como funciona cada guia:
  slug      -> nome do arquivo gerado (guia-<slug>.html). Use só letras minúsculas e hífen.
  titulo    -> aparece como H1 na página e no card
  resumo    -> 1-2 linhas, aparece no card da home e na descrição do Google
  categoria -> deve bater com uma das categorias do site (aparece como etiqueta)
  data      -> formato AAAA-MM-DD. Usado na ordenação e nos dados estruturados.
  destaque  -> True coloca o guia em evidência no topo da home. Deixe só UM como True.
  conteudo  -> o corpo do texto, em HTML simples (<p>, <h2>, <ul><li>, <strong>)

Dica: para criar um guia novo, copie um bloco inteiro, cole no fim da lista
e troque os campos.
"""

GUIAS = [
    {
        "slug": "enxoval-de-bebe-o-que-vale-comprar",
        "titulo": "Enxoval de bebê: o que realmente vale comprar",
        "resumo": "A lista de enxoval que circula por aí é enorme e boa parte não se usa. "
                  "Separamos o que sai da gaveta todo dia do que fica encostado.",
        "categoria": "Mundo do Bebê",
        "data": "2026-09-04",
        "destaque": True,
        "conteudo": """
<p>Toda lista de enxoval que a gente recebe na gravidez vem com umas 80 linhas. Depois que
o bebê nasce, você descobre que usa umas 20 de verdade — e que faltou coisa que ninguém
tinha avisado.</p>

<p>A ideia deste guia é simples: separar o que realmente entra na rotina do que só ocupa
espaço no armário. Nada aqui é regra, cada bebê é de um jeito, mas serve pra você não
gastar antes de saber se vai precisar.</p>

<h2>O que vale comprar antes do nascimento</h2>

<p><strong>Bodies de manga curta e comprida.</strong> É a peça que mais roda. Vale ter
bastante, porque troca de roupa é várias vezes por dia. Prefira os que abrem na frente
ou têm gola envelope — vestir pela cabeça de um recém-nascido é mais difícil do que parece.</p>

<p><strong>Macacões (mijões) de algodão.</strong> Confortáveis, fáceis de trocar fralda e
servem pra dormir e passear. Os de pezinho embutido evitam a meia que vive caindo.</p>

<p><strong>Panos de boca / fraldinhas de pano.</strong> Você vai usar pra tudo: proteger o
ombro, limpar, forrar. Parece exagero comprar uma dúzia, não é.</p>

<p><strong>Toalha com capuz.</strong> Duas ou três resolvem. O capuz não é enfeite: ajuda
a segurar o calor logo depois do banho.</p>

<h2>O que dá pra deixar pra depois</h2>

<p><strong>Sapatinhos.</strong> Recém-nascido não anda e não precisa de sapato. Meia
quentinha resolve o mesmo problema por bem menos.</p>

<p><strong>Roupa de tamanho RN em quantidade.</strong> Muitos bebês nascem já saindo do
RN, ou passam dele em três semanas. Compre poucas peças e reforce no tamanho P.</p>

<p><strong>Kit de higiene completo.</strong> Aqueles kits com dez itens costumam ter três
que você usa. Vale montar aos poucos.</p>

<p><strong>Berço com muitos acessórios.</strong> Protetores acolchoados, almofadas e
travesseiros dentro do berço não são recomendados para o sono do bebê — o berço deve ser
o mais livre possível.</p>

<h2>Onde vale gastar um pouco mais</h2>

<p>Duas categorias merecem atenção porque envolvem segurança e não dá pra economizar:</p>

<ul>
<li><strong>Cadeirinha para o carro.</strong> É obrigatória por lei e precisa ser adequada
ao peso e à altura da criança. Confira sempre a certificação do Inmetro e evite comprar
usada — não dá pra saber se já sofreu impacto.</li>
<li><strong>Berço.</strong> A distância entre as grades e a altura do estrado seguem norma
técnica. Berço certificado custa mais, mas é o lugar onde o bebê passa a maior parte do
tempo sozinho.</li>
</ul>

<h2>Uma dica que ninguém dá</h2>

<p>Não lave todo o enxoval de uma vez antes do parto. Deixe boa parte com etiqueta: se o
bebê pular de tamanho ou você ganhar peças repetidas de presente, dá pra trocar. Lave só
o que vai usar nas primeiras semanas.</p>
"""
    },
    {
        "slug": "brinquedos-seguros-por-idade",
        "titulo": "Brinquedo seguro: como escolher pela idade certa",
        "resumo": "A faixa etária na embalagem não é sugestão de esperteza da criança — "
                  "é indicação de segurança. Entenda o que ela quer dizer.",
        "categoria": "Mundo do Bebê",
        "data": "2026-09-03",
        "destaque": False,
        "conteudo": """
<p>Tem uma confusão comum na hora de comprar brinquedo: os pais olham o "3+" na caixa e
pensam "mas meu filho é esperto, dá conta". O problema é que essa marcação quase nunca
fala de inteligência — ela fala de <strong>risco físico</strong>.</p>

<h2>O que a faixa etária realmente indica</h2>

<p>Quando um brinquedo traz "não recomendado para menores de 3 anos", na maioria das vezes
é porque tem peça pequena que pode ser engolida ou aspirada. Até os 3 anos, a criança
explora tudo levando à boca, e essa é a fase de maior risco de engasgo.</p>

<p>A regra prática que dá pra usar em casa: se a peça passa por dentro de um tubo de papel
higiênico, ela é pequena o suficiente pra ser perigosa para um bebê.</p>

<h2>Por fase</h2>

<p><strong>Até 6 meses.</strong> Nessa fase o bebê quer contraste visual, som suave e
textura. Móbiles, chocalhos leves e mordedores de material atóxico. Nada com cordão longo
perto do berço.</p>

<p><strong>De 6 meses a 1 ano.</strong> Começa o "pegar, bater e levar à boca". Brinquedos
grandes, laváveis e sem peça destacável. Livrinhos de banho e de pano funcionam bem.</p>

<p><strong>De 1 a 3 anos.</strong> Empilhar, encaixar, empurrar. Blocos grandes,
brinquedos de puxar, instrumentos musicais simples. Ainda evitando peça pequena.</p>

<p><strong>A partir dos 3 anos.</strong> Aí entram os jogos com peças menores, quebra-cabeça,
massinha e brinquedos de montar. Se tiver irmão mais novo em casa, atenção redobrada — a
peça do mais velho vira risco pro menor.</p>

<h2>O que conferir na embalagem</h2>

<ul>
<li><strong>Selo do Inmetro.</strong> Brinquedo é produto com certificação compulsória no
Brasil. Sem selo, não compre.</li>
<li><strong>Indicação de material atóxico</strong>, principalmente em qualquer coisa que
vá à boca.</li>
<li><strong>Ausência de cordas e fitas longas</strong> em brinquedos para bebês — risco
de enrolar no pescoço.</li>
<li><strong>Pilhas com compartimento parafusado.</strong> Pilha botão é especialmente
perigosa se engolida.</li>
</ul>

<h2>Sobre brinquedo importado barato</h2>

<p>Vale um cuidado extra com produtos muito baratos vindos de fora sem certificação
nacional: tinta com metal pesado e plástico quebradiço são problemas reais nessa faixa.
Economizar aqui não compensa.</p>
"""
    },
    {
        "slug": "organizar-cozinha-pequena",
        "titulo": "Cozinha pequena: por onde começar a organizar",
        "resumo": "Antes de sair comprando organizador, tem uma etapa que quase todo mundo "
                  "pula — e é ela que faz a diferença.",
        "categoria": "Cozinha",
        "data": "2026-09-02",
        "destaque": False,
        "conteudo": """
<p>A tentação em cozinha apertada é comprar organizador. Você vê aquele vídeo com armário
perfeito, compra três potes e um suporte, e duas semanas depois está tudo bagunçado de
novo — só que agora com organizador no meio.</p>

<p>O que costuma faltar é a etapa anterior.</p>

<h2>Primeiro: tirar, não guardar</h2>

<p>Antes de comprar qualquer coisa, esvazie um armário por vez e separe o que você
<strong>realmente</strong> usou nos últimos seis meses. Aquele aparelho que ganhou de
presente, a forma de um formato específico, os potes sem tampa: isso ocupa o espaço que
falta pro que você usa toda semana.</p>

<p>Cozinha pequena não tem problema de organização, tem problema de volume. Organizador
não resolve excesso — só arruma o excesso de forma mais bonita.</p>

<h2>Depois: pensar por zona, não por categoria</h2>

<p>A lógica mais comum é guardar "tudo que é pote junto, tudo que é panela junto". Funciona
melhor agrupar por <strong>onde você usa</strong>:</p>

<ul>
<li>Perto do fogão: panelas, temperos, utensílios de cozimento, pegador</li>
<li>Perto da pia: escorredor, detergente, panos, lixeira</li>
<li>Perto da bancada de preparo: tábua, facas, tigelas, balança</li>
</ul>

<p>Isso reduz o vai-e-vem e, principalmente, aumenta a chance de você guardar de volta no
lugar certo.</p>

<h2>Aí sim: o que comprar</h2>

<p><strong>Organizadores empilháveis</strong> aproveitam a altura do armário, que é o
espaço mais desperdiçado. Meça a altura da prateleira antes — a foto do anúncio engana.</p>

<p><strong>Potes herméticos</strong> valem para grão, farinha e café. Os de vidro custam
mais, mas não retêm cheiro nem mancham com tempero, e duram muito mais que os de plástico.</p>

<p><strong>Suporte de parede ou barra com ganchos</strong> tira da gaveta os utensílios que
você usa todo dia. Em cozinha pequena, parede vazia é espaço desperdiçado.</p>

<p><strong>Organizador de pia</strong> resolve o acúmulo de esponja e detergente na
bancada, que é o que mais dá sensação de bagunça.</p>

<h2>Uma coisa que não vale</h2>

<p>Cuidado com kits enormes de potes de tamanhos variados. Você usa três tamanhos, no
máximo quatro. O resto vira aquele monte de tampa solta no fundo do armário.</p>
"""
    },
    {
        "slug": "casa-inteligente-por-onde-comecar",
        "titulo": "Casa inteligente: o básico que funciona de verdade",
        "resumo": "Dá pra começar com pouco e sentir diferença. Também dá pra gastar muito "
                  "em coisa que você usa duas semanas.",
        "categoria": "Tecnologia",
        "data": "2026-09-01",
        "destaque": False,
        "conteudo": """
<p>Automação residencial tem uma armadilha: os produtos mais chamativos costumam ser os
menos úteis no dia a dia, e os mais úteis são meio sem graça. Este guia é sobre o que
realmente muda a rotina.</p>

<h2>Antes de comprar qualquer coisa</h2>

<p>Confira a compatibilidade com o assistente que você já usa. Se sua casa tem Alexa, um
dispositivo que só funciona com Google Assistente vai te obrigar a abrir um app separado
toda vez — e é aí que você para de usar.</p>

<p>Fique atento também ao tipo de conexão. Dispositivos Wi-Fi conectam direto no roteador,
sem precisar de central (hub), o que é ótimo pra começar. A ressalva: cada um ocupa um
lugar na sua rede, então se você planeja ter dez ou mais, aí vale considerar um sistema
com hub.</p>

<h2>O que vale começar</h2>

<p><strong>Tomada inteligente.</strong> É o melhor custo-benefício da categoria. Você
transforma qualquer aparelho comum em programável — ventilador, luminária, cafeteira,
carregador. Serve pra desligar automaticamente coisa que você esquece ligada.</p>

<p><strong>Lâmpada inteligente.</strong> Funciona bem em ambiente onde você quer variar a
intensidade (quarto de bebê, sala à noite). Mas atenção a um detalhe: se alguém desligar
no interruptor da parede, ela fica inacessível pelo app.</p>

<p><strong>Sensor de porta ou de presença.</strong> Barato e resolve coisas concretas:
acender a luz do corredor quando alguém passa, avisar se a porta ficou aberta.</p>

<h2>O que costuma decepcionar</h2>

<p><strong>Fechadura inteligente</strong> em porta de apartamento com mais moradores. Se
uma pessoa da casa não usa, você acaba mantendo a chave normal em paralelo e o ganho some.</p>

<p><strong>Assistente de voz em cômodo barulhento.</strong> Cozinha com liquidificador e
TV ligada é o pior cenário pra reconhecimento de voz.</p>

<p><strong>Câmera interna sem pensar na privacidade.</strong> Vale checar se o fabricante
permite armazenamento local e se a gravação em nuvem é paga — muita câmera barata só
funciona bem com assinatura.</p>

<h2>O item mais subestimado</h2>

<p>Régua de tomadas com portas USB e organizador de fios. Não tem nada de inteligente,
custa pouco e resolve mais bagunça do dia a dia do que boa parte dos gadgets caros.</p>
"""
    },
]
