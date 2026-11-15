# Velurea — site em Django

Versão Django do site institucional da Velurea Clinic, com **painel de
administração** para editar o texto de todas as páginas e publicar posts no
blog.

O visual é o mesmo do site estático (`velurea-github-pages`): o CSS e o
JavaScript foram copiados sem alteração, e o HTML dos templates reproduz o
original classe por classe. O texto visível de todas as 21 páginas foi
comparado com o site estático e é idêntico.

---

## Rodar na sua máquina

Requer Python 3.12+.

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_site       # carrega o conteúdo do site estático
python manage.py createsuperuser
python manage.py runserver
```

- Site: http://localhost:8000
- Admin: http://localhost:8000/admin

Testes: `python manage.py test apps`

---

## O que o cliente edita no admin

| No admin | O que muda no site |
| --- | --- |
| **Configurações do site** | WhatsApp, e-mail, endereço, horário, texto do rodapé, faixa "Vamos avaliar o seu caso?" — vale para **todas** as páginas de uma vez |
| **Páginas** | Texto de cada seção de cada página (títulos, parágrafos, listas, imagens) e o título/descrição que aparecem no Google |
| **Tratamentos** | Os 10 tratamentos: cards da home, página de cada um, rodapé e lista do formulário |
| **Etapas do processo** | As 6 etapas (home e Como Funciona). A numeração 01, 02… é automática |
| **Diferenciais** | Home e Sobre |
| **Depoimentos** | Página de depoimentos; marque "mostrar na página inicial" para os 2 da home |
| **Perguntas frequentes** | FAQ |
| **Médicos parceiros** / **Hospitais e clínicas** | Página Médicos e Hospitais |
| **Blog → Posts / Categorias** | Artigos do blog, com editor visual |
| **Contatos recebidos** | Cada formulário enviado pelo site, com situação (novo, em atendimento…) e anotações internas |

Detalhes que valem saber:

- **Páginas e seções não se criam nem se apagam pelo admin**, só se editam: elas
  correspondem ao layout. Cada seção mostra só os campos que aparecem no site e
  diz, em "Campos usados", onde cada um entra.
- Nos campos de texto das seções, `**assim**` vira **negrito**. Listas são um
  item por linha; onde há título e texto na mesma linha, separe com `|`
  (ex.: `24/7 | Equipe local disponível…`).
- Imagem de seção em branco = continua a foto original do site.
- Itens de coleções têm **ordem** e **visível no site** — dá para ocultar sem apagar.
- **Posts**: rascunho não aparece no site; data futura agenda a publicação.
  Logado no admin, o link "pré-visualizar" mostra o post antes de publicar.
- **Campos clínicos dos tratamentos** (duração, permanência, candidatos) estão
  vazios de propósito e ficam recolhidos no admin. Só devem ser preenchidos com
  dado confirmado pela equipe médica; em branco, o site omite a seção.

---

## Diferenças em relação ao site estático

- **Formulário de contato**: antes ia para o Web3Forms; agora é salvo no banco
  (admin → Contatos recebidos) e gera um aviso por e-mail para o endereço das
  Configurações do site. Com o e-mail mal configurado, o contato não se perde.
  Tem proteção contra robôs (honeypot) e CSRF.
- **Blog**: cada post tem página própria (`/blog/<endereço>/`), categoria,
  capa e "Leia também". A lista mostra **8 posts por página**, com navegação
  numerada (`/blog/?pagina=2`). Os 4 posts do site estático só tinham título e
  resumo; ganharam texto completo (`apps/blog/seed_posts.py`), escrito a partir
  do que o site já afirma, sem dado clínico novo — **revisar com a equipe
  médica antes de divulgar**.
- **Página 404** traduzida para português (o original estava em inglês).
- **`/sitemap.xml`** e **`/robots.txt`** gerados automaticamente.
- **Modo demonstração**: "esconder o site do Google" (Configurações do site)
  liga o `noindex` e bloqueia tudo no robots.txt. Vem **ligado**, como no site
  estático atual. **Desligue ao publicar no domínio oficial.**

---

## Estrutura

```
config/                 settings, urls
apps/core/              configurações, páginas/seções, coleções, seed_site
apps/treatments/        tratamentos
apps/blog/              posts e categorias
apps/contact/           formulário e contatos recebidos
templates/              base.html (header/rodapé) + uma pasta por app
static/css/style.css    CSS original (Tailwind compilado) — não editar à mão
static/css/cms.css      estilos novos: corpo dos posts, erros do formulário
static/js/site.js       menu mobile + FAQ (original)
```

`style.css` é Tailwind já compilado: só existem nele as classes que o projeto
React usava. Classe Tailwind nova num template **não funciona** — escreva o
estilo em `cms.css`.

`seed_site` pode ser rodado de novo sem medo: cria só o que falta e nunca
sobrescreve texto editado no admin. `seed_site --reset` apaga o conteúdo e
recarrega o original (não apaga contatos nem usuários).

---

## Publicar

1. Copie `.env.example` para `.env` e preencha (`DJANGO_DEBUG=false`,
   `DJANGO_SECRET_KEY`, domínios, SMTP).
2. No servidor:
   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py seed_site
   python manage.py collectstatic --noinput
   python manage.py createsuperuser
   ```
3. Aponte o servidor WSGI para `config.wsgi:application` (gunicorn, ou
   "Setup Python App"/Passenger em hospedagem cPanel).
4. Os arquivos estáticos são servidos pelo próprio Django (WhiteNoise). Já os
   **uploads** (`media/`: capas de post, imagens de seção) precisam ser
   servidos pelo servidor web — configure `/media/` apontando para
   `DJANGO_MEDIA_ROOT`.
5. Faça backup de `db.sqlite3` e da pasta `media/`: é ali que mora todo o
   conteúdo editado pelo cliente.

SQLite atende bem um site institucional com um editor. Se um dia houver vários
editores simultâneos ou muito tráfego de escrita, troque por PostgreSQL em
`DATABASES`.
