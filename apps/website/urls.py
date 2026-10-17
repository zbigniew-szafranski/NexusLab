from django.urls import path

from . import views

app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
    path('cennik/', views.pricing, name='pricing'),
    path('kontakt/', views.contact, name='contact'),
    path('polityka-prywatnosci/', views.privacy, name='privacy'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
]
