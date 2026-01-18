# Egento-pa-6-projekt

Šestý projekt na Python Akademii od Engeta

## Popis projektu

Tento projekt jsou tři automatizované testy vytvořené pomocí frameworku Playwright k otestování stránky `engeto.cz`

## Instalace knihoven

Knihovny, které jsou použity v kódu jsou uložené v souboru `requirements.txt`. Pro instalaci doporučuji použít nové
virtuální prostředí a s nainstalovaným manažerem spustit následovně:

```bash
pip -- version                    # overim verzi manageru
pip install -r requirements.txt   # nainstalujeme knihovny
```

## Spuštění testů

Testy se pustí v rámci příkazového řádku:

```bash
python -m pytest -q
```

Případně pro spuštění i s prohlížečem:

```bash
pytest -q --headed
```