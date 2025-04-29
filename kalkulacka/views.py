from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .kalkulacka_lib import Kalkulacka

def kalkulacka_view(request):
    """
    Zobrazí úvodní stránku kalkulačky.
    """
    return render(request, 'kalkulacka/kalkulacka.html')

def vypocitej(request):
    """
    Zpracuje data z formuláře, provede výpočet pomocí třídy Kalkulacka
    a zobrazí výsledek.
    """
    if request.method == 'POST':
        try:
            cislo1 = float(request.POST.get('cislo1', 0))
            cislo2 = float(request.POST.get('cislo2', 0))
            operace = request.POST.get('operace')
            kalkulacka = Kalkulacka()  # Vytvoříme instanci třídy Kalkulacka
            vysledek = None

            if operace == 'secti':
                vysledek = kalkulacka.secti(cislo1, cislo2)
            elif operace == 'odecti':
                vysledek = kalkulacka.odecti(cislo1, cislo2)
            elif operace == 'vynasob':
                vysledek = kalkulacka.vynasob(cislo1, cislo2)
            elif operace == 'vydel':
                vysledek = kalkulacka.vydel(cislo1, cislo2)
            else:
                vysledek = "Neplatná operace!"

            return render(request, 'kalkulacka/kalkulacka.html', {
                'vysledek': vysledek,
                'cislo1': cislo1,
                'cislo2': cislo2,
                'operace': operace,
            })
        except ValueError:
            return render(request, 'kalkulacka/kalkulacka.html', {
                'chyba': 'Zadejte prosím platná čísla.',
            })
    else:
        return HttpResponseRedirect(reverse('kalkulacka'))