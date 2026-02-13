from django.contrib import admin

from .models import UserConfig, UserOffer


@admin.register(UserConfig)
class UserConfigAdmin(admin.ModelAdmin):
    list_display = ('user', 'lokalizacja', 'cena_min', 'cena_max', 'is_active')
    list_filter = ('is_active', 'lokalizacja', 'balkon', 'garaz', 'piwnica')
    search_fields = ('user__username', 'user__email', 'email')


@admin.register(UserOffer)
class UserOfferAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'price', 'area', 'rooms', 'sent_to_client', 'is_read', 'date_added')
    list_filter = ('sent_to_client', 'is_read', 'date_added')
    search_fields = ('user__username', 'title', 'offer_id')
    readonly_fields = ('date_added', 'date_scraped')
