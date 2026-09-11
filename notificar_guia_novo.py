# -*- coding: utf-8 -*-
"""
Notifica os inscritos da newsletter (Brevo) quando um guia novo aparece em
guias.py. Roda depois do gerador_site.py no atualizar.bat.

Como sabe o que é "novo": guias_notificados.json guarda os slugs que já
geraram e-mail. Guia com slug fora desse arquivo é considerado novo, dispara
a campanha, e o slug entra no arquivo pra nunca notificar de novo.

Precisa de BREVO_API_KEY num .env local (não versionado). Sem a chave, o
script não faz nada (deixa a geração do site seguir normalmente).
"""
import os
import json
import requests
from dotenv import load_dotenv
from guias import GUIAS

load_dotenv()

URL_SITE = "https://dicasdaely.com.br"
ARQUIVO_NOTIFICADOS = "guias_notificados.json"
LISTA_BREVO_ID = 2
REMETENTE_NOME = "Dicas da Ely"
REMETENTE_EMAIL = "contato@dicasdaely.com.br"


def carregar_notificados():
    if not os.path.exists(ARQUIVO_NOTIFICADOS):
        return set()
    with open(ARQUIVO_NOTIFICADOS, "r", encoding="utf-8") as f:
        return set(json.load(f))


def salvar_notificados(slugs):
    with open(ARQUIVO_NOTIFICADOS, "w", encoding="utf-8") as f:
        json.dump(sorted(slugs), f, ensure_ascii=False, indent=2)


def montar_html(guia):
    url_guia = f"{URL_SITE}/guia-{guia['slug']}.html"
    imagem_capa = f"{URL_SITE}/capas/capa-{guia['slug']}.png"
    return f"""
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #fdfbf7;">
  <img src="{imagem_capa}" alt="{guia['titulo']}" style="width: 100%; display: block; border-radius: 12px;">
  <div style="padding: 24px;">
    <span style="display: inline-block; background: #d35400; color: #fff; font-size: 12px;
                 font-weight: bold; text-transform: uppercase; padding: 4px 12px; border-radius: 20px;
                 margin-bottom: 12px;">Guia novo</span>
    <h1 style="color: #8c5e4a; font-size: 24px; margin: 8px 0;">{guia['titulo']}</h1>
    <p style="color: #5c4033; font-size: 16px; line-height: 1.6;">{guia['resumo']}</p>
    <p style="margin-top: 24px;">
      <a href="{url_guia}" style="background: #8c5e4a; color: #fff; padding: 12px 28px;
         border-radius: 30px; text-decoration: none; font-weight: bold; display: inline-block;">
        Ler o guia completo
      </a>
    </p>
  </div>
  <div style="padding: 16px 24px; border-top: 1px solid #eee5e0; font-size: 12px; color: #a89a90;">
    Você recebeu este e-mail porque se inscreveu em dicasdaely.com.br.
    <a href="{{{{ unsubscribe }}}}" style="color: #a89a90;">Cancelar inscrição</a>
  </div>
</div>
"""


def enviar_campanha(guia, chave_api):
    headers = {"api-key": chave_api, "content-type": "application/json"}

    payload_criar = {
        "sender": {"name": REMETENTE_NOME, "email": REMETENTE_EMAIL},
        "name": f"Guia novo: {guia['titulo']} ({guia['slug']})",
        "subject": f"Guia novo no Dicas da Ely: {guia['titulo']}",
        "htmlContent": montar_html(guia),
        "recipients": {"listIds": [LISTA_BREVO_ID]},
    }
    resposta = requests.post(
        "https://api.brevo.com/v3/emailCampaigns", headers=headers, json=payload_criar, timeout=30
    )
    resposta.raise_for_status()
    campanha_id = resposta.json()["id"]

    resposta_envio = requests.post(
        f"https://api.brevo.com/v3/emailCampaigns/{campanha_id}/sendNow", headers=headers, timeout=30
    )
    resposta_envio.raise_for_status()


def main():
    chave_api = os.getenv("BREVO_API_KEY")
    if not chave_api:
        print("BREVO_API_KEY não definida no .env, pulando notificação de guia novo.")
        return

    notificados = carregar_notificados()
    novos = [g for g in GUIAS if g["slug"] not in notificados]

    if not novos:
        print("📬 Nenhum guia novo pra notificar.")
        return

    for guia in novos:
        print(f"📬 Notificando guia novo por e-mail: {guia['titulo']}")
        try:
            enviar_campanha(guia, chave_api)
            notificados.add(guia["slug"])
        except Exception as e:
            print(f"⚠️  Falha ao notificar '{guia['slug']}': {e}")

    salvar_notificados(notificados)


if __name__ == "__main__":
    main()
