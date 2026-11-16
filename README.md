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

## Idiomas (PT · ES · EN · TR)

O site suporta português, espanhol, inglês e turco. Cada idioma além do
português é publicado quando a tradução estiver completa e revisada.

| Idioma | Situação |
| --- | --- |
| Português | original, sempre no ar |
| Español (neutro) | **traduzido por IA** (conteúdo e textos fixos) |
| English (EUA) | **traduzido por IA** (conteúdo e textos fixos) |
| Türkçe | **traduzido por IA** (conteúdo e textos fixos), tratamento formal ("siz") |

As traduções por IA são rascunho para a fase de desenvolvimento: **revisar
com tradutor antes do lançamento**.

Num banco novo, `seed_site` já carrega as traduções; para deixar um idioma
público, marque-o em **Configurações do site → Idiomas publicados**.

### Para quem traduz (admin)

1. Todo campo traduzível tem **abas por idioma** (PT-BR, ES, EN, TR). Preencha
   a aba do idioma; a aba PT-BR é o texto original.
2. Para revisar, abra o site com o prefixo do idioma **estando logado no
   admin**: `/es/`, `/en/`, `/tr/`. Uma faixa dourada indica a
   pré-visualização. Campo ainda sem tradução aparece em português.
3. Com tudo revisado, marque o idioma em **Configurações do site → Idiomas
   publicados**. A partir daí ele fica público, ganha seletor de idioma no
   header e no rodapé, entra no sitemap e nas tags `hreflang`.

**Quanto falta:** em Configurações do site, "Situação das traduções" mostra a
porcentagem de cada idioma. Nas listas do admin (Páginas, Tratamentos, Posts…),
a coluna **Traduções** marca cada item: `ES ✓` completo, `ES 3/5` parcial,
`ES –` sem tradução. O endereço (slug) não entra na conta.

O que **não** se traduz, de propósito: o texto dos depoimentos (fica no idioma
em que o paciente escreveu), nomes de pacientes e médicos, telefone e e-mail.

**Blog:** um post só aparece num idioma se tiver título naquele idioma. O blog
em espanhol não mostra artigos em português.

**Endereços:** o português não tem prefixo e mantém as URLs de sempre
(`/contato/`). Os outros idiomas usam prefixo e caminho traduzido
(`/es/contacto/`, `/en/contact/`, `/tr/iletisim/`). Tratamentos, posts e
categorias têm um campo "endereço" por idioma; em branco, usam o endereço em
português. Quem chega pelo endereço em português de algo que tem endereço
traduzido é redirecionado (301).

**Formulário:** cada contato registra o idioma em que foi enviado (aparece no
admin e no assunto do e-mail, ex.: `[ES]`), para a equipe responder na língua
do paciente. O tratamento é gravado sempre com o nome em português.

### Traduções em arquivo (`locale/content/<idioma>.json`)

O conteúdo do banco não vai para o repositório. Para uma tradução feita fora
do admin chegar a qualquer instalação, ela fica em
`locale/content/<idioma>.json`, carregado automaticamente pelo `seed_site`.
A importação **só preenche campos vazios**: nada escrito no admin é
sobrescrito.

```bash
python manage.py export_content -o para-traduzir.json   # texto em português
python manage.py import_content es                      # carrega es.json
python manage.py import_content es --overwrite          # substitui o que já existe
```

Cada registro é identificado pelo texto/endereço em português (ex.: a FAQ
pela pergunta, o tratamento pelo endereço). Se o português for reescrito no
admin, a tradução antiga deixa de ser aplicada — de propósito.

Nos posts, links internos precisam apontar para a versão do idioma
(`/es/contacto/`, não `/contato/`).

### Para desenvolvedores (textos fixos dos templates)

Textos que não estão no banco ("Ver detalhes", rótulos do formulário, menu)
usam o i18n do Django: `{% translate %}` nos templates e `gettext` no Python.
O texto em português é a própria chave. Traduções em
`locale/<idioma>/LC_MESSAGES/django.po`. Os `.mo` compilados são versionados
para o servidor não precisar do gettext.

Requer GNU gettext instalado (Windows: `winget install mlocati.GetText`).

```bash
python manage.py makemessages -l es -l en -l tr --ignore=.venv --no-obsolete
python manage.py compilemessages --ignore=.venv
```

Os trechos de URL estão nos mesmos arquivos, com contexto `url`
(`msgctxt "url"`). **Já estão traduzidos; mudá-los depois de publicado muda os
endereços do site.** Os três idiomas estão completos.

Com mais de um idioma publicado, o header desktop se ajusta para caber os
rótulos mais longos (turco: "Doktorlar ve Hastaneler"): o botão de WhatsApp
fica só com o ícone (o flutuante continua), os links do menu não quebram
linha e, entre 1280 e 1439px, ficam um pouco mais próximos.

Novos idiomas: acrescente em `LANGUAGES` e `apps/core/languages.py` (META),
rode `makemigrations` (o modeltranslation cria as colunas) e `makemessages`.

---

## Estrutura

```
config/                 settings, urls (rotas por idioma)
apps/core/              configurações, páginas/seções, coleções, seed_site,
                        idiomas (languages.py, middleware.py, translation.py,
                        content_translations.py)
apps/treatments/        tratamentos
apps/blog/              posts e categorias
apps/contact/           formulário e contatos recebidos
templates/              base.html (header/rodapé) + uma pasta por app
locale/                 traduções dos textos fixos (.po/.mo) e, em
                        locale/content/, do conteúdo do banco (.json)
static/css/style.css    CSS original (Tailwind compilado) — não editar à mão
static/css/cms.css      estilos novos: blog, formulário, seletor de idioma
static/js/site.js       menu mobile, FAQ e seletor de idioma
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
