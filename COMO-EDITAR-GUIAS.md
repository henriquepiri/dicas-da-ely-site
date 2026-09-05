# Como revisar e escrever os guias

Este arquivo é pra vocês dois. Nada aqui é código — é só como mexer nos textos.

---

## Por onde começar a revisão

Abra o arquivo `guias.py` no Bloco de Notas (ou VS Code, se preferir).
Cada guia é um bloco que começa assim:

```python
{
    "slug": "enxoval-de-bebe-o-que-vale-comprar",
    "titulo": "Enxoval de bebê: o que realmente vale comprar",
    ...
```

**O que vocês precisam ler com atenção:**

Escrevi os textos na primeira pessoa, como se fossem vocês falando ("nossa filha",
"na nossa casa", "a gente comprou"). Confiram se:

1. **Os fatos estão certos.** Onde escrevi que vocês compraram roupa RN demais, que
   sobrou fralda pequena, que testaram vários lenços e pomadas, que o canguru deixava
   a bebê em posição ruim, que o pato de luzes foi o brinquedo que mais chamou atenção —
   isso veio do que vocês me contaram. Se algum detalhe ficou torto, corrijam.

2. **O tom soa como vocês.** Se tem frase que vocês nunca falariam desse jeito, troquem.
   Texto que soa como a pessoa é o que diferencia de site genérico.

3. **As afirmações técnicas.** O guia do canguru fala em "posição em M" e queixo longe
   do peito. O de brinquedos fala de faixa etária e Inmetro. Escrevi com base em
   orientação geral bem estabelecida, mas como é conteúdo sobre segurança de bebê,
   vale confirmar com o pediatra antes de considerar publicado.

---

## Como editar um guia

Mexa só no que está entre aspas. Por exemplo, para mudar o título:

```python
"titulo": "Enxoval de bebê: o que realmente vale comprar",
```

vira

```python
"titulo": "Enxoval: o que a gente compraria de novo",
```

O texto do guia fica no campo `conteudo`, entre três aspas (`"""`). Lá dentro:

- `<p>parágrafo aqui</p>` — um parágrafo
- `<h2>Título de seção</h2>` — um subtítulo
- `<strong>palavra</strong>` — negrito
- `<ul><li>item</li><li>outro</li></ul>` — lista com marcadores

Não precisa decorar. Copiem o formato que já está lá.

---

## Como criar um guia novo

1. Copie um bloco inteiro (de `{` até `},`)
2. Cole logo antes do `]` no final do arquivo
3. Troque os campos:
   - `slug`: nome do arquivo, só minúsculas e hífen (ex: `primeiro-banho-do-bebe`)
   - `titulo`: o que aparece grande na página
   - `resumo`: 1-2 linhas, aparece no card e no Google
   - `categoria`: precisa ser igual a uma das categorias do site
     (Mundo do Bebê, Cozinha, Tecnologia, Casa & Decor, Cuidados Pessoais)
   - `data`: formato AAAA-MM-DD
   - `destaque`: deixe `False`. Só UM guia pode ter `True` (o que aparece no topo da home)
   - `conteudo`: o texto

---

## Depois de editar

No PowerShell, dentro da pasta do projeto:

```
python gerador_site.py
git add -A
git commit -m "Revisao dos textos dos guias"
git push
```

Em 1-2 minutos está no ar.

**Se der erro ao rodar o gerador**, quase sempre é aspas ou vírgula faltando. O erro
aponta a linha. Se travar, é só perguntar.

---

## Ideias de temas que ainda faltam

Coisas que vocês viveram e renderiam guia bom:

- Primeiro banho e os primeiros dias em casa
- O que levar na bolsa de maternidade (e o que sobra lá dentro)
- Voltar a trabalhar: organização e logística
- Passeio com bebê: o que realmente precisa ir junto
- Introdução alimentar: utensílios que ajudam

Um por semana, com história real dentro, vale mais que dez genéricos.

**Um aviso**: fórmula infantil, mamadeira, bico e chupeta têm restrição legal de
publicidade no Brasil (Lei 11.265/2006 - NBCAL). É por isso que a experiência de vocês
com leites e bicos ficou de fora dos guias. Se um dia quiserem abordar, vale consultar
alguém que entenda do assunto antes.
