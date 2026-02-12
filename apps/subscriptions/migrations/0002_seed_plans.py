from django.db import migrations


def seed_plans(apps, schema_editor):
    Plan = apps.get_model('subscriptions', 'Plan')
    Plan.objects.get_or_create(
        slug='darmowy',
        defaults={
            'name': 'Darmowy',
            'price': 0,
            'description': '7-dniowy darmowy test Gratka Alerts.',
            'features': [
                'Monitorowanie 1 lokalizacji',
                'Skanowanie co godzinę',
                'Powiadomienia email',
                'Dostęp do panelu Gratka Alerts',
            ],
            'display_order': 0,
        },
    )
    Plan.objects.get_or_create(
        slug='pro',
        defaults={
            'name': 'Pro',
            'price': 49,
            'description': 'Pełny dostęp do Gratka Alerts bez ograniczeń.',
            'features': [
                'Wszystko z planu Darmowego',
                'Nieograniczony dostęp',
                'Priorytetowe powiadomienia',
                'Wsparcie techniczne',
            ],
            'display_order': 1,
        },
    )


def reverse_plans(apps, schema_editor):
    Plan = apps.get_model('subscriptions', 'Plan')
    Plan.objects.filter(slug__in=['darmowy', 'pro']).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_plans, reverse_plans),
    ]
