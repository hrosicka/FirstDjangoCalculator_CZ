# JEDNODUCHÁ KALKULAČKA - DJANGO TUTORIAL V ČEŠTINĚ

Skvělý způsob, jak si procvičit základy toho frameworku krok za krokem.

![](https://github.com/hrosicka/FirstDjangoCalculator_CZ/blob/master/doc/svetly_rezim.PNG))

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

- **django-admin startproject jednoducha_kalkulacka:** Vytvoří nový Django projekt s názvem ```jednoducha_kalkulacka```.
- **cd jednoducha_kalkulacka:** Přepne tě do nově vytvořené složky projektu.
- **python manage.py startapp kalkulacka:** Vytvoří novou Django aplikaci s názvem ```kalkulacka``` uvnitř tvého projektu. Aplikace je modulární část tvého projektu, která se stará o specifickou funkcionalitu (v našem případě kalkulačku).

---

## 2. Definování URL adresy pro kalkulačku
Nyní musíme definovat, na jaké URL adrese bude naše kalkulačka dostupná. Otevři soubor ```jednoducha_kalkulacka/urls.py``` a uprav ho takto:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('kalkulacka/', include('kalkulacka.urls')),
]
```

Tento kód říká, že jakákoli URL adresa začínající ```/kalkulacka/``` bude směřována do souboru ```urls.py``` uvnitř naší aplikace ```kalkulacka```.

Nyní vytvoř soubor ```urls.py``` uvnitř složky ```kalkulacka``` a přidej do něj následující kód:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.kalkulacka, name='kalkulacka'),
    path('vypocitej/', views.vypocitej, name='vypocitej'),
]
```

Zde definujeme dvě URL adresy pro naši aplikaci:

- První **('')** odkazuje na úvodní stránku kalkulačky a je obsluhována funkcí ```kalkulacka``` v souboru ```views.py```.
- Druhá **('vypocitej/')** bude zpracovávat odeslaný formulář s čísly a operací a je obsluhována funkcí ```vypocitej``` v ```views.py```.

---

## 3. Vytvoření pohledů (Views)

Nyní se podíváme na soubor ```kalkulacka/views.py``` a definujeme funkce, které budou obsluhovat naše URL adresy:

```python
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

Funkce **kalkulacka** jednoduše vykreslí HTML šablonu s formulářem. Funkce ```vypocitej``` se spustí po odeslání formuláře:

- Zkontroluje, zda se jedná o metodu POST (data z formuláře).
- Získá hodnoty z formuláře (cislo1, cislo2, operace).
- Provádí zvolenou operaci.
- Předá výsledek (nebo chybovou zprávu) zpět do šablony pro zobrazení.
- Ošetřuje případné chyby při převodu vstupů na čísla (ValueError).
- Pokud se nejedná o POST požadavek, přesměruje uživatele zpět na úvodní stránku kalkulačky.

---

## 4. Vytvoření HTML šablony

Nyní musíme vytvořit HTML soubor, který bude obsahovat formulář pro zadání čísel a zobrazení výsledku. Vytvoř složku ```templates``` uvnitř složky ```kalkulacka``` a v ní složku ```kalkulacka``` a v ní soubor ```kalkulacka.html```. Do tohoto souboru vlož následující kód:

```html
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

- **{% csrf_token %}** je důležitý bezpečnostní prvek pro Django formuláře.
- **{% url 'vypocitej' %}** dynamicky generuje URL adresu pro pohled vypocitej.
- **{{ cislo1|default:'' }}** a podobně zobrazují předchozí zadané hodnoty, pokud existují.
- **{% if vysledek is not None %} a {% if chyba %}** podmíněně zobrazují výsledek nebo chybovou zprávu.

---

## 5. Registrace aplikace

Nesmíme zapomenout naši aplikaci zaregistrovat v souboru ```jednoducha_kalkulacka/settings.py```. Najdi sekci ```INSTALLED_APP```S a přidej do ní ```'kalkulacka'```:

```python
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

---

## 6. Spuštění vývojového serveru

Nyní můžeš spustit vývojový server Django a podívat se na svou kalkulačku v akci. V terminálu se ujisti, že jsi ve složce nejvyšší úrovně svého projektu (jednoducha_kalkulacka), a spusť příkaz:

```bash
python manage.py runserver
```
Otevři svůj webový prohlížeč a zadej adresu ```http://127.0.0.1:8000/kalkulacka/```. Měla by se ti zobrazit tvoje jednoduchá kalkulačka!

---

## 7. Jak udělat aplikaci hezkou?

### CSS soubor
- Vytvoř v adresáři aplikace ```kalkulacka``` (tam, kde máš ```views.py```, ```models.py``` atd.) nový adresář s názvem ```static```.
- Vytvoř v adresáři static další adresář s názvem ```kalkulacka```.
- Do adresáře ```static/kalkulacka``` ulož soubor s CSS styly. Můžeš ho pojmenovat například ```kalkulacka.css```.

https://github.com/hrosicka/FirstDjangoCalculator_CZ/blob/master/kalkulacka/static/kalkulacka/kalkulacka.css

### Vložení odkazu do HTML
Nyní, když máš CSS soubor uložený na správném místě, musíš do svého HTML souboru (```kalkulacka.html```) vložit odkaz na něj. Odkaz se vkládá do hlavičky dokumentu, tedy mezi tagy ```<head>``` a ```</head>```.

Ujisti se, že máš na začátku souboru ```{% load static %}``` a že odkaz na CSS vypadá takto
 ```code
{% load static %}
<!DOCTYPE html>
<html lang="cs">
<head>
    ...
    <link rel="stylesheet" href="{% static 'kalkulacka/kalkulacka.css' %}">
    ...
</head>
<body>
    ...
</body>
</html>
```

---

## 8. Oddělení logiky výpočtu

Oddělení logiky výpočtu do samostatné třídy je skvělý způsob, jak zlepšit organizaci a čitelnost kódu. Uděláme to takto:

- Vytvoříme třídu ```Kalkulacka```, která obsahuje metody pro jednotlivé aritmetické operace (secti, odecti, vynasob, vydel).
- Funkce ```vypocitej``` nyní vytvoří instanci této třídy a volá příslušnou metodu pro provedení výpočtu.
- Základní logika výpočtu je přesunuta do třídy, což zlepšuje strukturu kódu a usnadňuje jeho údržbu a testování.
- Přejmenuj funkci kalkulacka na kalkulacka_view, aby bylo jasnější, že se jedná o pohled (view) v Django.

---

## 9. Třída Kalkulacka v samostatném souboru

To je standardní postup pro udržení čisté struktury projektu. Třídu ```Kalkulacka``` přesuneme do samostatného souboru a ukážeme si, jak ji pak importovat do ```views.py```.
Tímto způsobem oddělíš logiku výpočtů od logiky zpracování požadavků a zlepšíš organizaci svého kódu.

- **Vytvoř soubor kalkulacka_lib.py:** Vytvoř nový soubor s názvem ```kalkulacka_lib.py``` v adresáři aplikace kalkulacka (tam, kde máš ```views.py```).
- **Přesuň třídu Kalkulacka:** Přesuň kód třídy Kalkulacka z ```views.py``` do ```kalkulacka_lib.py```.
- **Importuj třídu v ```views.py:```** V souboru ```views.py``` přidej řádek from ```.kalkulacka_lib import Kalkulacka```, který importuje třídu z nového souboru.

```python
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .kalkulacka_lib import Kalkulacka
```

---


## 10. Světlý a tmavý režim aplikace

Přidáme přepínač motivu (světlý/tmavý) a uložíme preferované nastavení do localStorage, takže se motiv zachová i po obnovení stránky.

![](https://github.com/hrosicka/FirstDjangoCalculator_CZ/blob/master/doc/tmavy_rezim.PNG))


### Soubor ```kalkulacka.css```

- Otevři soubor ```kalkulacka.css```.
- Uprav ho nádledujícím způsobem
  
```css
:root {
    --background-color: #f3f4f6;
    --text-color: #4a5568;
    --primary-color: #3b82f6;
    --primary-hover-color: #2563eb;
    --secondary-color: #fff;
    --border-color: #e2e8f0;
    --shadow-color: rgba(0, 0, 0, 0.1);
    --input-focus-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

body {
    font-family: 'Inter', sans-serif;
    background-color: var(--background-color);
    color: var(--text-color);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    margin: 0;
    padding: 20px;
    transition: background-color 0.3s ease;
}

.calculator-wrapper {
    background-color: var(--secondary-color);
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px -1px var(--shadow-color), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    padding: 2rem;
    width: 100%;
    max-width: 400px;
    transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

h1 {
    color: var(--text-color);
    text-align: center;
    margin-bottom: 1.5rem;
    font-size: 1.75rem;
    transition: color 0.3s ease;
}

form {
    margin-bottom: 1rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
    color: #718096;
    font-weight: 600;
    font-size: 1rem;
}

input[type="number"], select {
    box-sizing: border-box;
    width: 100%;
    padding: 0.75rem;
    border: 1px solid var(--border-color);
    border-radius: 0.375rem;
    margin-bottom: 1rem;
    font-size: 1rem;
    transition: border-color 0.15s ease-in-out, shadow-sm 0.15s ease-in-out, background-color 0.3s ease, color 0.3s ease;
    background-color: var(--secondary-color);
    color: var(--text-color);
}

input[type="number"]:focus, select:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: var(--input-focus-shadow);
}

select {
    appearance: none;
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20' fill='none' stroke='currentColor' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'%3e%3cpath d='M6 9l4 4 4-4'%3e%3c/path%3e%3c/svg%3e");
    background-repeat: no-repeat;
    background-position: right 0.75rem center;
    background-size: 1rem;
    padding-right: 2.5rem;
}

button {
    background-color: var(--primary-color);
    color: var(--secondary-color);
    padding: 0.75rem 1.5rem;
    border-radius: 0.375rem;
    border: none;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.15s ease-in-out, transform 0.1s ease-in-out, shadow-sm 0.15s ease-in-out, color 0.3s ease;
    width: 100%;
    display: block;
    margin: 0 auto;
}

button:hover {
    background-color: var(--primary-hover-color);
}

button:active {
    transform: translateY(2px);
    box-shadow: none;
}

button:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
}

h2 {
    color: var(--text-color);
    text-align: center;
    margin-top: 1.5rem;
    font-size: 1.5rem;
    transition: color 0.3s ease;
}

.error-message {
    color: #dc2626;
    text-align: center;
    margin-top: 1rem;
    font-size: 1rem;
}

.theme-switch-wrapper {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    margin-bottom: 1rem;
}

.theme-switch-label {
    display: inline-block;
    margin-right: 0.5rem;
    color: var(--text-color);
    font-size: 0.875rem;
    transition: color 0.3s ease;
}

.theme-switch {
    position: relative;
    display: inline-block;
    width: 4rem;
    height: 2rem;
}

.theme-switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    border-radius: 2rem;
    transition: .4s;
}

.slider:before {
    position: absolute;
    content: "";
    height: 1.5rem;
    width: 1.5rem;
    left: 0.25rem;
    bottom: 0.25rem;
    background-color: white;
    border-radius: 50%;
    transition: .4s;
}

input:checked + .slider {
    background-color: var(--primary-color);
}

input:focus + .slider {
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
}

input:checked + .slider:before {
    transform: translateX(2rem);
}

/* Dark mode styles */
.dark-mode {
    --background-color: #1a202c;
    --text-color: #f7fafc;
    --primary-color: #68d391;
    --primary-hover-color: #48bb78;
    --secondary-color: #2d3748;
    --border-color: #4a5568;
    --shadow-color: rgba(255, 255, 255, 0.1);
}
```


### Soubor ```kalkulacka.html```

- Otevři soubor ```kalkulacka.html```.
- Najdi řádek ```<body>``` a vlož pod něj následující kód:


```html
<div class="theme-switch-wrapper">
    <label for="theme-switch" class="theme-switch-label">Světlý/tmavý režim:</label>
    <label class="theme-switch">
        <input type="checkbox" id="theme-switch">
        <span class="slider round"></span>
    </label>
</div>
```

- Přidej na konec souboru, před uzavírací tag ```</body>```, následující kód:
  
```html
<script>
const themeSwitch = document.getElementById('theme-switch');
const body = document.body;

const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    body.classList.add(savedTheme);
    if (savedTheme === 'dark-mode') {
        themeSwitch.checked = true;
    }
}

themeSwitch.addEventListener('change', () => {
    body.classList.toggle('dark-mode');
    if (body.classList.contains('dark-mode')) {
        localStorage.setItem('theme', 'dark-mode');
    } else {
        localStorage.setItem('theme', '');
    }
});

</script>
```

---

## 11. Přesun JavaSctipt do samostatného souboru
Přesunutí JavaScriptu do samostatného souboru je často lepší praxe. Tímto způsobem oddělíš JavaScript od HTML, což je lepší pro organizaci kódu a údržbu.

- **Vytvoř soubor ```kalkulacka.js```:** Vytvoř nový soubor s názvem ```kalkulacka.js``` v adresáři static/kalkulacka/.
- **Přesuň JavaScript kód:** Přesuň JavaScript kód z HTML souboru (```kalkulacka.html```) do souboru ```kalkulacka.js```.
- **Odkazuj na JavaScript soubor:** V HTML souboru (```kalkulacka.html```) přidej před uzavírací tag ```</body> tag <script>``` s atributem ```src```, který odkazuje na tvůj soubor ```kalkulacka.js```.

kalkulacka.js:

```js
const themeSwitch = document.getElementById('theme-switch');
const body = document.body;

const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    body.classList.add(savedTheme);
    if (savedTheme === 'dark-mode') {
        themeSwitch.checked = true;
    }
}

themeSwitch.addEventListener('change', () => {
    body.classList.toggle('dark-mode');
    if (body.classList.contains('dark-mode')) {
        localStorage.setItem('theme', 'dark-mode');
    } else {
        localStorage.setItem('theme', '');
    }
});

```

kalkulacka.html:

```html
{% load static %}
<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jednoduchá Kalkulačka</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'kalkulacka/kalkulacka.css' %}">
    <script src="https://unpkg.com/tone"></script>
</head>
<body>
    <div class="calculator-wrapper">
        <div class="theme-switch-wrapper">
            <label for="theme-switch" class="theme-switch-label">Světlý/tmavý režim:</label>
            <label class="theme-switch">
                <input type="checkbox" id="theme-switch">
                <span class="slider round"></span>
            </label>
        </div>
        <h1>Jednoduchá Kalkulačka</h1>

        <form method="post" action="{% url 'vypocitej' %}">
            {% csrf_token %}
            <label for="cislo1">Číslo 1:</label>
            <input type="number" name="cislo1" id="cislo1" value="{{ cislo1|default:'' }}" placeholder="Zadejte první číslo">

            <label for="cislo2">Číslo 2:</label>
            <input type="number" name="cislo2" id="cislo2" value="{{ cislo2|default:'' }}" placeholder="Zadejte druhé číslo">

            <label for="operace">Operace:</label>
            <select name="operace" id="operace">
                <option value="secti" {% if operace == 'secti' %}selected{% endif %}>+</option>
                <option value="odecti" {% if operace == 'odecti' %}selected{% endif %}>-</option>
                <option value="vynasob" {% if operace == 'vynasob' %}selected{% endif %}>*</option>
                <option value="vydel" {% if operace == 'vydel' %}selected{% endif %}>/</option>
            </select>

            <button type="submit">Vypočítat</button>
        </form>

        {% if vysledek is not None %}
            <h2>Výsledek: {{ vysledek }}</h2>
        {% endif %}

        {% if chyba %}
            <p class="error-message">{{ chyba }}</p>
        {% endif %}
    </div>
    <script src="{% static 'kalkulacka/kalkulacka.js' %}"></script>
</body>
</html>
```

