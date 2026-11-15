"""Configuração do site Velurea.

Tudo o que muda entre máquina local e servidor vem de variáveis de ambiente,
lidas de um arquivo `.env` na raiz quando ele existe (veja `.env.example`).
"""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def env_bool(name: str, default: bool = False) -> bool:
    return os.environ.get(name, str(default)).strip().lower() in {"1", "true", "yes", "sim"}


def env_list(name: str, default: str = "") -> list[str]:
    return [v.strip() for v in os.environ.get(name, default).split(",") if v.strip()]


DEBUG = env_bool("DJANGO_DEBUG", True)

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")
if not SECRET_KEY:
    if not DEBUG:
        raise RuntimeError("Defina DJANGO_SECRET_KEY no ambiente de produção.")
    SECRET_KEY = "dev-only-insecure-key-nao-use-em-producao"

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,[::1]")
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")

INSTALLED_APPS = [
    # modeltranslation precisa vir antes do admin para registrar as abas.
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "tinymce",
    "apps.core",
    "apps.treatments",
    "apps.blog",
    "apps.contact",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Depois da autenticação: precisa de request.user para liberar a
    # pré-visualização de idiomas ainda não publicados.
    "apps.core.middleware.LanguageGateMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.site",
            ],
            "builtins": ["django.templatetags.i18n", "apps.core.templatetags.velurea"],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get("DJANGO_DB_PATH", BASE_DIR / "db.sqlite3"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

TIME_ZONE = "Europe/Istanbul"
USE_TZ = True

# ------------------------------------------------------------- idiomas ---
# O português é o idioma padrão e fica sem prefixo na URL (/contato/), como
# sempre foi. Os demais ganham prefixo e endereços traduzidos (/es/contacto/).
#
# Estar nesta lista NÃO publica o idioma: ele só aparece para o público depois
# de marcado em Configurações do site → "Idiomas publicados". Até lá, só quem
# está logado no admin consegue ver (pré-visualização).
LANGUAGE_CODE = "pt-br"
LANGUAGES = [
    ("pt-br", "Português"),
    ("es", "Español"),
    ("en", "English"),
    ("tr", "Türkçe"),
]
USE_I18N = True
LOCALE_PATHS = [BASE_DIR / "locale"]

# Campos traduzidos pelo admin (django-modeltranslation). Campo vazio num
# idioma mostra o português — rede de segurança enquanto a tradução não termina.
MODELTRANSLATION_DEFAULT_LANGUAGE = "pt-br"
MODELTRANSLATION_FALLBACK_LANGUAGES = ("pt-br",)

# URLs do site original terminam em barra (/contato/); APPEND_SLASH redireciona
# /contato para /contato/, então os dois formatos continuam funcionando.
APPEND_SLASH = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = Path(os.environ.get("DJANGO_MEDIA_ROOT", BASE_DIR / "media"))

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage"
            if DEBUG
            else "whitenoise.storage.CompressedManifestStaticFilesStorage"
        )
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Uploads do admin (fotos de posts e seções). Acima disso o Django recusa.
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

# ---------------------------------------------------------------- e-mail ---
# Sem EMAIL_HOST definido, os e-mails de novo contato são impressos no
# terminal em vez de enviados — útil para desenvolver sem servidor SMTP.
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_BACKEND = (
    "django.core.mail.backends.smtp.EmailBackend"
    if EMAIL_HOST
    else "django.core.mail.backends.console.EmailBackend"
)
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL", "Site Velurea <nao-responda@velureaistanbul.com>"
)

# ------------------------------------------------------------ segurança ---
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = env_bool("DJANGO_SSL_REDIRECT", True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# --------------------------------------------------------------- TinyMCE ---
# Editor do corpo dos posts do blog. Barra enxuta de propósito: o visual do
# site vem do CSS, então o editor oferece estrutura (títulos, listas, links,
# imagens), não cores nem fontes.
TINYMCE_DEFAULT_CONFIG = {
    "height": 520,
    "menubar": False,
    "plugins": "link lists image autolink code wordcount",
    "toolbar": (
        "undo redo | blocks | bold italic | bullist numlist | blockquote | "
        "link image | removeformat | code"
    ),
    "block_formats": "Parágrafo=p; Título=h2; Subtítulo=h3",
    "relative_urls": False,
    "branding": False,
    "promotion": False,
    "license_key": "gpl",
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {"apps": {"handlers": ["console"], "level": "INFO"}},
}
