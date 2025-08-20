Jornal da Operação – Flipbook (Django)

Um protótipo completo para publicar semanalmente o “Jornal da Operação” como um flipbook web a partir de um PDF (manter o fluxo atual do Google Slides → exporta PDF → upload no sistema). Inclui backend em Django, conversão de PDF em imagens com pdf2image/Pillow, front-end com Turn.js e persistência histórica em Postgres 16 (Docker).

1) Estrutura de pastas
jornal_flipbook/
├─ manage.py
├─ .env
├─ requirements.txt
├─ README.md
├─ jornal_operacao/                # projeto Django
│  ├─ __init__.py
│  ├─ settings.py                  # Configurações principais
│  ├─ urls.py                      # Roteamento global
│  ├─ wsgi.py                      # Interface WSGI
│  └─ asgi.py                      # Interface ASGI
└─ boletim/                        # app principal
   ├─ __init__.py
   ├─ admin.py
   ├─ apps.py
   ├─ forms.py
   ├─ models.py
   ├─ signals.py                   # Sinais pós-upload
   ├─ views.py
   ├─ urls.py                      # URLs do app
   ├─ templates/
   │  ├─ base.html
   │  ├─ issue_list.html
   │  ├─ issue_upload.html
   │  └─ issue_detail.html
   └─ static/
      ├─ css/style.css
      └─ js/turn.min.js            # (usando CDN no template; opcional baixar aqui)

2) Arquivo .env (exemplo)
Em Windows, se o Poppler não estiver no PATH, defina POPPLER_PATH no .env para garantir que a conversão funcione.
3) manage.py
4) jornal_operacao/settings.py
5) jornal_operacao/urls.py
6) jornal_operacao/wsgi.py
7) jornal_operacao/asgi.py
8) boletim/apps.py
9) boletim/models.py
10) boletim/signals.py (conversão PDF → imagens ao salvar)
11) boletim/forms.py
12) boletim/admin.py
13) boletim/views.py
14) boletim/urls.py
15) Templates
16) static/css/style.css
17) Management Command – reconstruir páginas
# Jornal da Operação – Flipbook (Django)

Publicador web do Jornal da Operação a partir de um PDF. Faz o upload do PDF, converte páginas em imagens e exibe em um flipbook.

## Requisitos
- Python 3.10+
- Docker
- Poppler instalado no sistema (necessário para pdf2image)

## Setup rápido
```bash
python -m venv .venv
. .venv/bin/activate   # Linux/macOS
# ou
.venv\\Scripts\\activate # Windows

pip install -r requirements.txt


cp .env.example .env  # ou crie seu .env com credenciais
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
python manage.py runserver
Home: http://127.0.0.1:8000/

Upload: http://127.0.0.1:8000/upload/

Admin: http://127.0.0.1:8000/admin/

Fluxo semanal

Exportar Google Slides como PDF.

Acessar /upload/ e enviar o PDF, preenchendo: título, semana, data início/fim.

Após salvar, o sistema converte automaticamente e você visualiza a edição em flipbook.

Histórico fica disponível na Home (edições anteriores).
Poppler (Windows)

Baixe os binários do Poppler e adicione o caminho .../bin ao PATH.

Qualidade das páginas: ajuste dpi em boletim/signals.py (200–300). Se o PDF vier com imagens comprimidas, 220–240 costuma equilibrar nitidez e tamanho.

Compressão das imagens: o Pillow já salva com quality=85 e optimize=True. Se quiser mais leve, teste quality=80.

Lazy loading: Turn.js carrega imagens conforme a navegação, mas para versões muito longas, considere paginar em lotes (ex.: mostrar 10 páginas e carregar próximas on‑demand).

Cache/headers: com Whitenoise, já há cache fingerprinted para estáticos. Para mídia, configure Nginx/
CDN com Cache-Control: public, max-age=31536000, immutable em /media/issues/*.

Acessibilidade: adicione alt/aria-label nas páginas (exibindo número e título da edição) e teclas de atalho (← →) para navegar.

Mobile/gestos: ative swipe/touch (Turn.js já suporta). Evite imagens muito grandes no mobile; use CSS responsivo.

SEO/OG: inclua metatags Open Graph e twitter:card para compartilhar o link da edição.

Segurança: desative DEBUG em produção; limite ALLOWED_HOSTS; considere autenticação
(ex.: apenas logado pode subir PDF; lojas só leem). Se necessário, token para URLs públicas.

Fila (opcional): para PDFs grandes, mova a conversão para Celery + Redis e mostre um status de processamento.

Armazenamento: se o histórico crescer, troque MEDIA_ROOT por S3/compatível via django-storages.
https://www.turnjs.com/#