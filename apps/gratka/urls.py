from django.urls import path

from . import views

app_name = 'gratka'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('zapisz/', views.save_config, name='save_config'),
]
