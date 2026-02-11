from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('', include('apps.gratka.urls')),
    path('gratka/', RedirectView.as_view(url='/', permanent=False)),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
]
