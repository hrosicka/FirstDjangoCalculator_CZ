from django.urls import path
from . import views

urlpatterns = [
    path('', views.kalkulacka_view, name='kalkulacka'),
    path('vypocitej/', views.vypocitej, name='vypocitej'),
]