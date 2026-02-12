from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


TRIAL_DURATION_DAYS = 7


class Plan(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    description = models.TextField(blank=True)
    features = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'subscriptions_plan'
        ordering = ['display_order']

    def __str__(self):
        return f"{self.name} ({self.price} PLN)"


class UserSubscription(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscription',
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subscribers',
    )
    trial_start = models.DateTimeField(default=timezone.now)
    trial_end = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subscriptions_usersubscription'

    def save(self, *args, **kwargs):
        if not self.trial_end:
            self.trial_end = self.trial_start + timedelta(days=TRIAL_DURATION_DAYS)
        super().save(*args, **kwargs)

    @property
    def is_trial_active(self):
        return timezone.now() < self.trial_end

    @property
    def has_access(self):
        return self.is_active or self.is_trial_active

    def __str__(self):
        status = "aktywna" if self.has_access else "wygasła"
        return f"{self.user.email} — {status}"
