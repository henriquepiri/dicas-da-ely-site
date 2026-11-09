@echo off
cd /d C:\Users\Pichau\dicas-da-ely-site
python gerador_site.py
git add -A
git commit -m "Atualizacao do site"
git push
python notificar_guia_novo.py
