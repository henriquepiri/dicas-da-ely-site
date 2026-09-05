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
        "resumo": "Compramos roupa RN demais e sobrou fralda pequena. O que a gente aprendeu "
                  "na prática sobre o que vale comprar antes do bebê nascer.",
        "categoria": "Mundo do Bebê",
        "data": "2026-09-04",
        "destaque": True,
        "conteudo": """
<p>Toda lista de enxoval que a gente recebe na gravidez vem com umas 80 linhas. Depois que
nossa filha nasceu, descobrimos que usávamos umas 20 de verdade — e que tinha coisa
faltando que ninguém tinha avisado.</p>

<p>Este guia é o que a gente gostaria de ter lido antes. Não é regra, cada bebê é de um
jeito. É o que aconteceu na nossa casa.</p>

<h2>O erro que a gente cometeu (e quase todo mundo comete)</h2>

<p><strong>Compramos roupa RN demais.</strong> Muita. E o bebê passa desse tamanho rápido
demais — algumas peças a gente usou duas, três vezes. Outras nem chegaram a sair da
gaveta com etiqueta.</p>

<p>A mesma coisa aconteceu com <strong>fralda de tamanho pequeno</strong>. Compramos
pacotes grandes achando que estávamos economizando, e sobrou fralda que não servia mais.</p>

<p>Se for pra levar uma coisa só deste guia, leve esta: <strong>compre pouco dos tamanhos
iniciais</strong>. Poucas peças RN, um pacote pequeno de fralda P. Você reabastece em dois
dias se precisar — e não fica com armário cheio de coisa que não serve.</p>

<h2>Não abra tudo de uma vez</h2>

<p>Ligado ao ponto acima: deixe boa parte do enxoval com etiqueta e o pacote de fralda
fechado. Se o bebê pular de tamanho, se você ganhar peça repetida de presente, ou se a
marca de fralda não servir bem no corpo dele, dá pra trocar. Depois de lavado ou aberto,
não dá.</p>

<h2>O que realmente rodou na nossa rotina</h2>

<p><strong>Bodies.</strong> É a peça que mais gira, disparado. Troca de roupa acontece
várias vezes por dia. Prefira os que abrem na frente ou de gola envelope — vestir pela
cabeça de um recém-nascido é mais difícil do que parece.</p>

<p><strong>Macacões de algodão.</strong> Servem pra dormir e pra sair. Os de pezinho
embutido evitam a meia que vive caindo.</p>

<p><strong>Panos de boca.</strong> A gente usou pra tudo: proteger o ombro, limpar, forrar,
cobrir. Uma dúzia não é exagero.</p>

<p><strong>Toalha com capuz.</strong> Duas ou três resolvem. O capuz não é enfeite, ajuda
a segurar o calor na saída do banho.</p>

<h2>As coisas que a gente testou até achar</h2>

<p>Tem uma categoria de item que você não consegue acertar de primeira, por mais que
pesquise. Com a gente foi assim:</p>

<p><strong>Lenço umedecido.</strong> Testamos vários. Muda muito de marca pra marca —
espessura, quantidade de umidade, cheiro. Alguns esfarelam, outros vêm secos demais.</p>

<p><strong>Pomada de assadura.</strong> Também testamos várias até achar a que funcionava
bem na pele dela.</p>

<p>A dica prática aqui: <strong>compre a menor embalagem primeiro</strong>. Não caia na
tentação do pacote gigante "que sai mais barato" antes de saber se serve. Sai caro
descobrir que não deu certo com um estoque de seis meses em casa.</p>

<h2>Onde não dá pra economizar</h2>

<p>Duas coisas envolvem segurança e merecem atenção diferente:</p>

<ul>
<li><strong>Cadeirinha para o carro.</strong> É obrigatória por lei, precisa ser adequada
ao peso e à altura, e deve ter certificação do Inmetro. Evite comprar usada — não dá pra
saber se já sofreu impacto.</li>
<li><strong>Berço.</strong> A distância entre as grades e a altura do estrado seguem norma
técnica. É onde o bebê passa mais tempo sozinho.</li>
</ul>

<p>Sobre o berço, vale um lembrete: protetores acolchoados, almofadas e travesseiros
soltos lá dentro não são recomendados para o sono do bebê. O berço deve ficar o mais
livre possível.</p>
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

<h2>O que prendeu atenção de verdade na nossa casa</h2>

<p>Vale contar antes: o brinquedo que mais chamou a atenção da nossa filha foi um
<strong>pato cheio de luzes que toca música alta</strong>. Nada sofisticado, nada
educativo-com-selo. Luz piscando e som.</p>

<p>Isso diz uma coisa útil sobre bebê: nessa fase, o que engaja é estímulo sensorial
direto — luz, som, textura, contraste. Brinquedo caro de madeira com proposta pedagógica
tem seu valor, mas costuma render mais alguns meses depois.</p>

<p>O contraponto honesto: som alto perto do ouvido de bebê incomoda e, em volume muito
alto, não faz bem. Vale checar se o brinquedo tem controle de volume antes de comprar —
muitos não têm.</p>

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
    {
        "slug": "canguru-como-escolher-posicao-correta",
        "titulo": "Canguru e sling: como saber se a posição está certa",
        "resumo": "Testamos alguns que deixavam a bebê numa posição ruim. O que olhar "
                  "antes de comprar e como conferir depois que já está no corpo.",
        "categoria": "Mundo do Bebê",
        "data": "2026-09-05",
        "destaque": False,
        "conteudo": """
<p>Essa foi uma das nossas frustrações: compramos canguru achando que era só vestir e
pronto, e testamos mais de um que deixava a bebê numa posição claramente ruim — pernas
penduradas, corpo curvado, peso mal distribuído.</p>

<p>Demorou pra gente entender que existe diferença técnica real entre modelos, e que a
maioria dos cangurus baratos de loja tem o mesmo problema.</p>

<h2>O problema dos modelos mais simples</h2>

<p>Muito canguru barato sustenta o bebê só pela virilha, deixando as pernas caídas para
baixo, como se ele estivesse pendurado. Todo o peso fica concentrado num ponto pequeno.</p>

<p>A recomendação de fisioterapeutas e pediatras vai no sentido oposto: o ideal é que a
coxa fique apoiada até a dobra do joelho, com os joelhos mais altos que o bumbum — o
formato que costumam chamar de <strong>posição em M</strong> ou "posição de sapinho".
Nessa posição o peso se distribui pelo quadril inteiro em vez de ficar todo na virilha.</p>

<h2>Como conferir na prática</h2>

<p>Depois de colocar, olhe estes pontos:</p>

<ul>
<li><strong>Joelhos mais altos que o bumbum</strong>, formando um M. Se as pernas estão
retas pra baixo, o modelo não está apoiando direito.</li>
<li><strong>Coxa apoiada até o joelho</strong>, não só a virilha.</li>
<li><strong>Costas levemente arredondadas</strong>, respeitando a curva natural — não
esticadas à força nem dobradas demais.</li>
<li><strong>Queixo longe do peito.</strong> Deve caber pelo menos um dedo entre o queixo
e o peitoral do bebê. Queixo colado dificulta a respiração, e esse é o ponto mais
importante da lista.</li>
<li><strong>Rosto visível.</strong> Você deve conseguir ver o rosto sem afastar tecido.</li>
<li><strong>Perto o suficiente pra beijar</strong> a cabeça do bebê sem se esticar. Se
está mais baixo que isso, está frouxo demais.</li>
<li><strong>Ajustado, não folgado.</strong> Bebê solto dentro do canguru escorrega e
curva o corpo.</li>
</ul>

<h2>Antes de comprar</h2>

<p>Confira a <strong>faixa de peso</strong> indicada pelo fabricante e se o modelo tem
apoio de cabeça — nos primeiros meses, quando o bebê ainda não sustenta o pescoço, isso
não é opcional.</p>

<p>Verifique também se dá pra ajustar em quem vai usar. Cangurus de tamanho único
costumam ficar bem em uma pessoa da casa e mal na outra.</p>

<p>Se puder, experimente antes ou compre de lugar com política de troca clara. É um item
que só dá pra avaliar de verdade com o bebê dentro.</p>

<h2>Um aviso</h2>

<p>Este guia é a nossa experiência somada ao que se recomenda de forma geral sobre
posicionamento. Não substitui orientação de pediatra ou fisioterapeuta — se você notar
qualquer desconforto, choro ao ser colocado, ou tiver dúvida sobre o quadril do seu bebê,
converse com quem acompanha ele.</p>
"""
    },
    {
        "slug": "fralda-como-escolher-e-quanto-comprar",
        "titulo": "Fralda: como escolher o tamanho e quanto comprar",
        "resumo": "A conta que quase todo mundo erra no começo, e por que estocar "
                  "tamanho pequeno costuma dar prejuízo.",
        "categoria": "Mundo do Bebê",
        "data": "2026-09-06",
        "destaque": False,
        "conteudo": """
<p>Fralda é o item que mais consome dinheiro no primeiro ano, e também é onde a gente
mais errou a conta. Vale escrever sobre isso.</p>

<h2>O erro de estocar tamanho pequeno</h2>

<p>Parece lógico: fralda é consumo garantido, então comprar pacote grande sai mais barato.
O problema é que o bebê muda de tamanho rápido, e principalmente nos primeiros meses.</p>

<p>Compramos pacotes grandes de tamanho pequeno e sobrou fralda que não servia mais. O
dinheiro que a gente "economizou" no preço por unidade virou fralda encostada.</p>

<p>A regra que funcionou depois: <strong>pacote pequeno nos tamanhos iniciais, pacote
grande só a partir do momento em que o bebê estabiliza num tamanho</strong> — o que
costuma acontecer alguns meses depois.</p>

<h2>Tamanho não é idade, é peso</h2>

<p>As embalagens trazem faixa de peso, e é isso que vale. Dois bebês da mesma idade podem
usar tamanhos diferentes. Se a fralda está marcando a perna ou vazando com frequência,
provavelmente já passou da hora de subir.</p>

<p>Um detalhe: dentro da mesma faixa de peso, a modelagem muda de marca para marca. Uma
que veste bem no seu bebê pode ser justamente a que vaza no do vizinho.</p>

<h2>Testar antes de decidir</h2>

<p>Como acontece com lenço e pomada, fralda também é item de tentativa e erro. Vale
comprar embalagens pequenas de duas ou três marcas antes de fechar com uma.</p>

<p>O que observar em cada teste:</p>

<ul>
<li><strong>Vazamento</strong>, principalmente à noite e em fralda de cocô</li>
<li><strong>Marca na pele</strong> na cintura e nas pernas</li>
<li><strong>Absorção</strong> — se fica pesada e mole rápido demais</li>
<li><strong>Reação na pele</strong>, que varia bastante entre marcas</li>
</ul>

<h2>Sobre a fralda noturna</h2>

<p>Algumas marcas têm linha específica para a noite, com mais absorção. Costuma custar
mais caro por unidade, e uma estratégia razoável é usar a comum de dia e a reforçada só
à noite, em vez de pagar o preço maior o tempo todo.</p>

<h2>Quanto comprar por mês</h2>

<p>O consumo cai bastante ao longo do primeiro ano — recém-nascido troca muito mais vezes
por dia do que um bebê de oito meses. Então não use o consumo do primeiro mês como base
para estocar.</p>

<p>Na prática: acompanhe seu próprio consumo por duas semanas antes de comprar em
quantidade. É mais confiável que qualquer tabela genérica.</p>
"""
    },
    {
        "slug": "quarto-de-bebe-pequeno",
        "titulo": "Quarto de bebê pequeno: o que cabe e o que não precisa",
        "resumo": "Dá pra montar um quarto funcional em pouco espaço. O truque é saber "
                  "o que dos móveis tradicionais realmente faz falta.",
        "categoria": "Casa & Decor",
        "data": "2026-09-07",
        "destaque": False,
        "conteudo": """
<p>As fotos de quarto de bebê que circulam mostram berço grande, cômoda, poltrona de
amamentação, tapete, prateleiras. Em quarto pequeno — ou em quarto compartilhado com os
pais — nada disso cabe junto.</p>

<p>A boa notícia é que boa parte desses móveis não é essencial.</p>

<h2>O que realmente faz falta</h2>

<p><strong>Um lugar seguro pra dormir.</strong> Berço, mini-berço ou berço de canto.
Modelos menores existem e cumprem a mesma função nos primeiros meses. O que não muda é a
exigência de segurança: certificação, distância entre grades, estrado firme.</p>

<p><strong>Uma superfície pra trocar fralda.</strong> Não precisa ser trocador móvel. Um
colchonete de troca sobre a cômoda que você já tem, ou sobre a cama, resolve. O que
importa é ter tudo à mão — nunca dá pra soltar o bebê pra pegar algo.</p>

<p><strong>Onde guardar roupa.</strong> Roupa de bebê é pequena e cabe em pouco espaço.
Gaveteiro estreito ou até caixas organizadoras numa prateleira dão conta.</p>

<h2>O que costuma ser dispensável</h2>

<p><strong>Poltrona de amamentação.</strong> É confortável, ocupa muito espaço e custa
caro. Muita gente acaba amamentando na cama mesmo. Se o quarto é apertado, essa é a
primeira coisa a cortar.</p>

<p><strong>Trocador com móvel próprio.</strong> Vira mesa de bagunça em poucos meses e
perde a função quando o bebê começa a rolar.</p>

<p><strong>Cômoda grande.</strong> Enxoval de bebê ocupa menos do que parece, ainda mais
se você seguir a lógica de comprar pouco dos tamanhos iniciais.</p>

<h2>Aproveitar altura em vez de área</h2>

<p>Em quarto pequeno, o espaço que sobra é vertical. Prateleiras acima do trocador ou da
cômoda deixam à mão o que você usa todo dia, sem ocupar chão.</p>

<p>Um cuidado importante: nada pesado ou de vidro em prateleira acima de onde o bebê fica.
E fixação bem feita na parede, não em fita adesiva — a mesma prateleira que hoje segura
fralda pode virar apoio de criança que aprendeu a subir.</p>

<h2>Deixe espaço vazio</h2>

<p>Parece contraintuitivo, mas vale planejar chão livre. Em poucos meses o bebê vai
querer rolar, engatinhar e brincar no chão, e aí um tapete e espaço aberto valem mais que
qualquer móvel decorativo.</p>
"""
    },
]
