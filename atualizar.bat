@echo off
cd /d C:\Users\Pichau\dicas-da-ely-site
python robo_coletor.py
python gerador_site.py
git add -A
git commit -m "Atualizacao automatica diaria"
git push
