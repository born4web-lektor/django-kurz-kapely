# django-kurz-kapely — vzorová aplikace Django kurzu

Vzorová aplikace (kapely, alba, písně) ke kurzu **django-kurz-basic**. Vznikla z appky
`kapely` toho kurzu a na školení slouží jako „hotový výsledek" — to, co během kurzu
tvoříme. Kurz samotný (výklad, scénáře, studijní materiály) žije v repu `django-kurz-basic`.

## Stack
Python 3.12, Django 4.2 (stará verze — plánovaný upgrade spolu s kurzem), SQLite,
`django-extensions`, `django-bootstrap-v5`, pytest + pytest-django. Závislosti
v `requirements.txt` (pip, žádné Poetry; `psycopg2-binary` zbyl z konfigurace pro deployment).

## Struktura
```
bandbase/         # projekt: settings, urls, obecné views
bands/            # appka: modely Genre/Band/Album/Song/Artist, views, formuláře, šablony
  fixtures/       # data (žánry, kapely, alba, písně) — načítá je migrace 0001
  management/     # vlastní manage.py příkazy (ukázky)
tests/            # pytest; soubory s prefixem X jsou vypnuté
pm.sh, pms.sh     # zkratky: python -m manage / shell_plus
```

## Jak se aplikace používá (důležité pro úpravy kódu)
- **Kód je výukový.** Vedle sebe záměrně žijí varianty téhož (FBV → generické `View`
  → CBV, ruční formulář → `ModelForm`). Neslučovat a nemazat „duplicity".
- Změny držet v souladu s kurzem `django-kurz-basic` (appka `kapely` + `_lektor/`).
- Testovací DB: `TEST_DB=True` přepne settings na `test_db.sqlite3` (viz `tests/conftest.py`).
  `test_check_existing_model_instances` dnes 3× padá — parametry testu neodpovídají
  fixtures (Metallica 1981 vs 1982, The Clash ve fixtures chybí); zatím neřešeno.
- Fixtures obsahují jen veřejná data o kapelách; žádné reálné osobní údaje.

## Příkazy
```bash
source .venv/bin/activate
python manage.py migrate          # vytvoří DB včetně dat z fixtures
python manage.py runserver
python manage.py shell_plus
pytest
```
Nový stroj: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`.

## Git
Jediná větev `main`. Remoty `github` (born4web-lektor) + `lobogit` (lobito-lektor) — push do obou.

## Projektová dokumentace
`.claude/ISSUE.md` (úkoly), `.claude/SESSION_LOG.md` (historie session).
