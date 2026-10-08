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
