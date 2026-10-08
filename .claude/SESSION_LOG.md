# Session Log

---

## 2026-10-08

**Téma:** Onboarding repa pro práci s Claude Code (kurz = přenosný projekt, evidence v KB portfoliu)

**Co se řešilo:**
- Remoty sjednoceny na `github` (born4web-lektor) + `lobogit` (lobito-lektor); lobogit repo existovalo prázdné → první push `main`.
- `.venv` (Python 3.12) + `requirements.txt`; ověřeno `manage.py check`, `migrate`, `runserver` (`/` 200, `/admin/` → login).
- `CLAUDE.md` (standalone, bez AI-OS includů), `.claudeignore`, README, `.claude/ISSUE.md` + `SESSION_LOG.md`.
- `pytest`: 3 passed, 3 failed (`test_check_existing_model_instances` — data testu ≠ fixtures), zapsáno do ISSUE.

**Rozhodnutí:**
- Kurz = přenosný projekt, evidence v KB `projects/portfolio.md`, ne v AI-OS manifestu.
- `.claude/ISSUE.md` a `SESSION_LOG.md` verzované; ignoruje se jen `.claude/settings.local.json`.

---

## 2026-10-08 (2)

**Téma:** Upgrade na Django 5.2 LTS (postup z `django-kurz-basic`)

**Co se řešilo:**
- `Django==5.2.18`, `django-bootstrap-v5` → `django-bootstrap5==26.3` (appka `django_bootstrap5`, `{% load django_bootstrap5 %}`, `django_bootstrap5/bootstrap5.html`), `django-extensions==4.1`, pytest 9.1.1, pytest-django 4.14.0; `requirements.txt` jen přímé závislosti.
- Ověřeno na kopii: smoke test 29 URL (anonym + admin) na 4.2 i 5.2 identický, 0 chyb; `makemigrations --check` bez změn; pytest 3 passed / 3 failed stejně jako před upgradem (známý problém v ISSUE).
- `AccountLogoutView` je vlastní `RedirectView` volající `logout()` — změna `LogoutView` na POST v Django 5.0 se ho netýká.

**Stav:** větev `upgrade-django52`, nepushnuto.

