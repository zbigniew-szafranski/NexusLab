from django.contrib import admin

from .models import Plan, UserSubscription


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'is_active', 'display_order')
    list_editable = ('is_active', 'display_order')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'trial_start', 'trial_end', 'is_active', 'has_access_display')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('user__email',)
    readonly_fields = ('trial_start', 'trial_end', 'created_at', 'updated_at')

    @admin.display(boolean=True, description='Ma dostęp?')
    def has_access_display(self, obj):
        return obj.has_access
