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

## 2. Definování URL adresy pro kalkulačku
Nyní musíme definovat, na jaké URL adrese bude naše kalkulačka dostupná. Otevři soubor jednoducha_kalkulacka/urls.py a uprav ho takto:

```code
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('kalkulacka/', include('kalkulacka.urls')),
]
```

Tento kód říká, že jakákoli URL adresa začínající /kalkulacka/ bude směřována do souboru urls.py uvnitř naší aplikace kalkulacka.

---

## 2. Definování URL adresy pro kalkulačku
Nyní musíme definovat, na jaké URL adrese bude naše kalkulačka dostupná. Otevři soubor jednoducha_kalkulacka/urls.py a uprav ho takto:

```code
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('kalkulacka/', include('kalkulacka.urls')),
]
```

Tento kód říká, že jakákoli URL adresa začínající /kalkulacka/ bude směřována do souboru urls.py uvnitř naší aplikace kalkulacka.

Nyní vytvoř soubor urls.py uvnitř složky kalkulacka a přidej do něj následující kód:
```code
from django.urls import path
from . import views

urlpatterns = [
    path('', views.kalkulacka, name='kalkulacka'),
    path('vypocitej/', views.vypocitej, name='vypocitej'),
]
```

Zde definujeme dvě URL adresy pro naši aplikaci:

- První **('')** odkazuje na úvodní stránku kalkulačky a je obsluhována funkcí kalkulacka v souboru views.py.
- Druhá **('vypocitej/')** bude zpracovávat odeslaný formulář s čísly a operací a je obsluhována funkcí vypocitej v views.py.

---

## 3. Vytvoření pohledů (Views)

Nyní se podíváme na soubor kalkulacka/views.py a definujeme funkce, které budou obsluhovat naše URL adresy:

```code
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

def kalkulacka(request):
    return render(request, 'kalkulacka/kalkulacka.html')

def vypocitej(request):
    if request.method == 'POST':
        try:
            cislo1 = float(request.POST.get('cislo1', 0))
            cislo2 = float(request.POST.get('cislo2', 0))
            operace = request.POST.get('operace')
            vysledek = None

            if operace == 'secti':
                vysledek = cislo1 + cislo2
            elif operace == 'odecti':
                vysledek = cislo1 - cislo2
            elif operace == 'vynasob':
                vysledek = cislo1 * cislo2
            elif operace == 'vydel':
                if cislo2 != 0:
                    vysledek = cislo1 / cislo2
                else:
                    vysledek = "Nelze dělit nulou!"

            return render(request, 'kalkulacka/kalkulacka.html', {'vysledek': vysledek, 'cislo1': cislo1, 'cislo2': cislo2, 'operace': operace})
        except ValueError:
            return render(request, 'kalkulacka/kalkulacka.html', {'chyba': 'Zadejte prosím platná čísla.'})
    else:
        return HttpResponseRedirect(reverse('kalkulacka'))
```

Funkce **kalkulacka** jednoduše vykreslí HTML šablonu s formulářem. Funkce vypocitej se spustí po odeslání formuláře:

- Zkontroluje, zda se jedná o metodu POST (data z formuláře).
- Získá hodnoty z formuláře (cislo1, cislo2, operace).
- Provádí zvolenou operaci.
- Předá výsledek (nebo chybovou zprávu) zpět do šablony pro zobrazení.
- Ošetřuje případné chyby při převodu vstupů na čísla (ValueError).
- Pokud se nejedná o POST požadavek, přesměruje uživatele zpět na úvodní stránku kalkulačky.

---

## 4. Vytvoření HTML šablony

Nyní musíme vytvořit HTML soubor, který bude obsahovat formulář pro zadání čísel a zobrazení výsledku. Vytvoř složku templates uvnitř složky kalkulacka a v ní soubor kalkulacka.html. Do tohoto souboru vlož následující kód:

```code
<!DOCTYPE html>
<html>
<head>
    <title>Jednoduchá Kalkulačka</title>
</head>
<body>
    <h1>Jednoduchá Kalkulačka</h1>

    <form method="post" action="{% url 'vypocitej' %}">
        {% csrf_token %}
        <label for="cislo1">Číslo 1:</label>
        <input type="number" name="cislo1" id="cislo1" value="{{ cislo1|default:'' }}"><br><br>

        <label for="cislo2">Číslo 2:</label>
        <input type="number" name="cislo2" id="cislo2" value="{{ cislo2|default:'' }}"><br><br>

        <label for="operace">Operace:</label>
        <select name="operace" id="operace">
            <option value="secti" {% if operace == 'secti' %}selected{% endif %}>+</option>
            <option value="odecti" {% if operace == 'odecti' %}selected{% endif %}>-</option>
            <option value="vynasob" {% if operace == 'vynasob' %}selected{% endif %}>*</option>
            <option value="vydel" {% if operace == 'vydel' %}selected{% endif %}>/</option>
        </select><br><br>

        <button type="submit">Vypočítat</button>
    </form>

    {% if vysledek is not None %}
        <h2>Výsledek: {{ vysledek }}</h2>
    {% endif %}

    {% if chyba %}
        <p style="color: red;">{{ chyba }}</p>
    {% endif %}
</body>
</html>
```

Tento HTML kód vytvoří jednoduchý formulář s dvěma číselnými poli, rozbalovacím menu pro výběr operace a tlačítkem pro odeslání.

- {% csrf_token %} je důležitý bezpečnostní prvek pro Django formuláře.
- {% url 'vypocitej' %} dynamicky generuje URL adresu pro pohled vypocitej.
- {{ cislo1|default:'' }} a podobně zobrazují předchozí zadané hodnoty, pokud existují.
- {% if vysledek is not None %} a {% if chyba %} podmíněně zobrazují výsledek nebo chybovou zprávu.

---

## 5. Registrace aplikace

Nesmíme zapomenout naši aplikaci zaregistrovat v souboru jednoducha_kalkulacka/settings.py. Najdi sekci INSTALLED_APPS a přidej do ní 'kalkulacka':
```code
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'kalkulacka',  # Přidali jsme naši aplikaci
]
```
