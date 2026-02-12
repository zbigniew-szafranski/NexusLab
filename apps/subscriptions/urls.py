from django.urls import path

from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('wygaslo/', views.trial_expired, name='trial_expired'),
]
