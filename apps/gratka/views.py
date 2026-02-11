from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import UserConfigForm
from .models import UserConfig, UserOffer


@login_required
def dashboard(request):
    config = UserConfig.objects.filter(user=request.user).first()
    form = UserConfigForm(instance=config)
    if not config:
        form.initial['email'] = request.user.email

    offers = UserOffer.objects.filter(user=request.user)[:20]

    return render(request, 'gratka/dashboard.html', {
        'form': form,
        'config': config,
        'offers': offers,
    })


@login_required
def save_config(request):
    if request.method != 'POST':
        return render(request, 'gratka/partials/config_success.html', {
            'error': 'Nieprawidłowe żądanie.',
        })

    config = UserConfig.objects.filter(user=request.user).first()
    form = UserConfigForm(request.POST, instance=config)

    if form.is_valid():
        user_config = form.save(commit=False)
        user_config.user = request.user
        user_config.save()
        return render(request, 'gratka/partials/config_success.html', {
            'config': user_config,
            'success': True,
        })

    return render(request, 'gratka/partials/config_success.html', {
        'form': form,
        'error': 'Popraw błędy w formularzu.',
    })
