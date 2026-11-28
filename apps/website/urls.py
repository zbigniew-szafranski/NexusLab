from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
    path('realizacje/flowmail/', views.case_flowmail, name='case_flowmail'),
    path('realizacje/zamowienia-b2b/', views.case_b2b_orders, name='case_b2b_orders'),
    path('realizacje/zamawianie-posilkow/', views.case_meal_orders, name='case_meal_orders'),
    # Gratka Alerts pricing lives on its own subdomain; keep old links working
    path('cennik/', RedirectView.as_view(url='https://gratka.nexuslab.pl/cennik/', permanent=True), name='pricing'),
    path('kontakt/', views.contact, name='contact'),
    path('polityka-prywatnosci/', views.privacy, name='privacy'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
]
