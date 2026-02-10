from django.contrib.auth.models import User
from django.db import models


class UserConfig(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lokalizacja = models.CharField(max_length=100, default='lodz')
    cena_min = models.IntegerField(default=100000)
    cena_max = models.IntegerField(default=250000)
    metraz_min = models.IntegerField(null=True, blank=True)
    metraz_max = models.IntegerField(null=True, blank=True)
    balkon = models.BooleanField(default=True)
    garaz = models.BooleanField(default=True)
    piwnica = models.BooleanField(default=False)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'gratka_userconfig'
        verbose_name = 'User Config'
        verbose_name_plural = 'User Configs'

    def __str__(self):
        return f"{self.user.username} - {self.lokalizacja}"


class UserOffer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers')
    offer_id = models.CharField(max_length=50)
    url = models.TextField()
    full_link = models.TextField()
    title = models.TextField()
    price = models.CharField(max_length=100, blank=True)
    area = models.CharField(max_length=50, blank=True)
    rooms = models.CharField(max_length=50, blank=True)
    floor = models.CharField(max_length=50, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_scraped = models.DateTimeField(auto_now_add=True)
    sent_to_client = models.BooleanField(default=False)

    class Meta:
        db_table = 'gratka_useroffer'
        verbose_name = 'User Offer'
        verbose_name_plural = 'User Offers'
        unique_together = ['user', 'offer_id']
        ordering = ['-date_added']

    def __str__(self):
        return f"{self.title} ({self.offer_id})"
