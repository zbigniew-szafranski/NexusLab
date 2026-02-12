from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.website.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('gratka/', include('apps.gratka.urls')),
    path('chatbot/', include('apps.chatbot.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('subskrypcja/', include('apps.subscriptions.urls')),
]
