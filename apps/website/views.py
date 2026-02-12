from django.shortcuts import render

from apps.subscriptions.models import Plan


def home(request):
    return render(request, 'website/index.html')


def pricing(request):
    plans = Plan.objects.filter(is_active=True)
    return render(request, 'website/pricing.html', {'plans': plans})
