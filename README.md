# django-kurz-kapely

Vzorová aplikace (kapely, alba, písně) ke kurzu
[`django-kurz-basic`](https://github.com/born4web-lektor/django-kurz-basic) — výsledek toho,
co se na kurzu tvoří.

## Spuštění

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate      # vytvoří DB včetně dat
python manage.py runserver
```

Aplikace běží na <http://127.0.0.1:8000/>. Testy: `pytest`.
