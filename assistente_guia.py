# -*- coding: utf-8 -*-
"""
Assistente de texto pros guias (opcional) — usa a API da OpenAI pra ajudar a
revisar um guia existente ou rascunhar um novo, sempre a partir de fatos reais
que vocês fornecem.

NUNCA escreve direto em guias.py: gera um arquivo de sugestão em sugestoes/
pra vocês lerem, ajustarem e colarem à mão. A decisão final do texto continua
sendo de vocês — ver COMO-EDITAR-GUIAS.md.

Uso:
  python assistente_guia.py revisar <slug-do-guia>
      Lê o conteúdo atual desse guia em guias.py e devolve uma versão mais
      fluida, no mesmo tom, sem inventar fato novo. Slug é o mesmo campo
      "slug" do bloco em guias.py.

  python assistente_guia.py novo <arquivo-com-topicos.txt>
      Lê um .txt com o tema e os pontos reais que aconteceram com vocês (um
      por linha) e devolve um rascunho de guia pronto pra revisar e colar
      em guias.py.

Precisa de uma chave da OpenAI num arquivo .env (não versionado, veja
.env.example) com:
  OPENAI_API_KEY=sk-...
"""
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from guias import GUIAS

load_dotenv()

MODELO = "gpt-4o-mini"
PASTA_SUGESTOES = "sugestoes"

VOZ_DO_SITE = """Você escreve para o site Dicas da Ely, de um casal (Elyad e
Henrique) que compartilha experiências reais como pais de uma criança pequena.

Regras de tom, inegociáveis:
- Primeira pessoa do plural ("a gente", "nossa filha", "na nossa casa").
- Só use fatos que foram dados a você no pedido. NUNCA invente uma
  experiência, produto, marca, número ou situação que não esteja no
  material fornecido. Se faltar informação pra uma frase, deixe mais vaga
  em vez de inventar um detalhe.
- Português do Brasil informal, direto, sem clichê de blog ("nesse artigo
  você vai descobrir", "confira nossa seleção", "não deixe de conferir").
- Frases curtas. Prefira concretude a generalidade: "sobrou fralda P" em
  vez de "compramos itens em excesso".
- HTML simples apenas: <p>, <h2>, <strong>, <ul><li>. Nada de markdown,
  <script> ou blocos de código.
- Nunca use travessão/hífen longo (—) pra ligar frases. É um tique clássico
  de texto gerado por IA. Troque por ponto, vírgula ou dois-pontos.
- Nunca mencione fórmula infantil, mamadeira, bico ou chupeta, nem
  recomende marca desses itens — têm restrição legal de publicidade no
  Brasil (Lei 11.265/2006, NBCAL)."""


def cliente():
    chave = os.getenv("OPENAI_API_KEY")
    if not chave:
        print("Erro: defina OPENAI_API_KEY no arquivo .env (veja .env.example).")
        sys.exit(1)
    return OpenAI(api_key=chave)


def salvar_sugestao(nome, texto):
    os.makedirs(PASTA_SUGESTOES, exist_ok=True)
    carimbo = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho = os.path.join(PASTA_SUGESTOES, f"{nome}_{carimbo}.txt")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"\n✅ Sugestão salva em: {caminho}")
    print("   Leia com calma, confirme que os fatos batem, ajuste o tom e só")
    print("   então cole em guias.py na mão.")


def revisar(slug):
    guia = next((g for g in GUIAS if g["slug"] == slug), None)
    if not guia:
        print(f"Não achei nenhum guia com slug '{slug}' em guias.py.")
        print("Slugs existentes:")
        for g in GUIAS:
            print(f"  - {g['slug']}")
        sys.exit(1)

    prompt = f"""Aqui está o texto atual do guia "{guia['titulo']}":

{guia['conteudo']}

Reescreva deixando mais fluido e natural, mantendo TODOS os fatos, histórias
e a estrutura de seções como estão — não corte nem adicione nenhuma
informação. Só melhore a forma de contar. Devolva só o HTML do campo
"conteudo", pronto pra colar, sem comentário nenhum antes ou depois."""

    resposta = cliente().chat.completions.create(
        model=MODELO,
        messages=[
            {"role": "system", "content": VOZ_DO_SITE},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )
    salvar_sugestao(f"revisao_{slug}", resposta.choices[0].message.content)


def novo(caminho_topicos):
    if not os.path.exists(caminho_topicos):
        print(f"Arquivo não encontrado: {caminho_topicos}")
        sys.exit(1)
    with open(caminho_topicos, "r", encoding="utf-8") as f:
        topicos = f.read().strip()

    if not topicos:
        print("O arquivo de tópicos está vazio.")
        sys.exit(1)

    prompt = f"""Com base SÓ nestes tópicos reais que aconteceram com o casal:

{topicos}

Escreva um rascunho de guia completo, nesta ordem:
1. Um título (1 linha, sem HTML)
2. Um resumo de 1-2 linhas (sem HTML)
3. O corpo em HTML (<p>, <h2>, <strong>, <ul><li>), com pelo menos 2 seções
   com <h2>, no mesmo espírito dos outros guias do site: conta o que
   aconteceu, o que aprenderam, e fecha com uma recomendação prática.

Separe as 3 partes com uma linha "---". Não invente nenhum fato que não
esteja nos tópicos acima."""

    resposta = cliente().chat.completions.create(
        model=MODELO,
        messages=[
            {"role": "system", "content": VOZ_DO_SITE},
            {"role": "user", "content": prompt},
        ],
        temperature=0.8,
    )
    nome_base = os.path.splitext(os.path.basename(caminho_topicos))[0]
    salvar_sugestao(f"novo_guia_{nome_base}", resposta.choices[0].message.content)


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("revisar", "novo"):
        print(__doc__)
        sys.exit(1)

    comando, alvo = sys.argv[1], sys.argv[2]
    if comando == "revisar":
        revisar(alvo)
    else:
        novo(alvo)


if __name__ == "__main__":
    main()
