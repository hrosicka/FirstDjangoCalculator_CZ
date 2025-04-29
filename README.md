# JEDNODUCHÁ KALKULAČKA - DJANGO TUTORIAL V ČEŠTINĚ

Skvělý způsob, jak si procvičit základy toho frameworku krok za krokem.

---

## 1. Vytvoření Django projektu a aplikace
Nejprve si otevři svůj terminál nebo příkazovou řádku a přejdi do složky, kde chceš svůj projekt vytvořit. 
Potom spusť následující příkazy:
```bash
django-admin startproject jednoducha_kalkulacka
cd jednoducha_kalkulacka
python manage.py startapp kalkulacka
```

Tyto příkazy udělají následující:

- **django-admin startproject jednoducha_kalkulacka:** Vytvoří nový Django projekt s názvem jednoducha_kalkulacka.
- **cd jednoducha_kalkulacka:** Přepne tě do nově vytvořené složky projektu.
- **python manage.py startapp kalkulacka:** Vytvoří novou Django aplikaci s názvem kalkulacka uvnitř tvého projektu. Aplikace je modulární část tvého projektu, která se stará o specifickou funkcionalitu (v našem případě kalkulačku).

---
