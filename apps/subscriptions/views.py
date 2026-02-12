from django.shortcuts import render


def trial_expired(request):
    return render(request, 'subscriptions/trial_expired.html')
