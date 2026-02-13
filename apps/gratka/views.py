from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import UserConfigForm
from .models import UserConfig, UserOffer


@login_required
def dashboard(request):
    config = UserConfig.objects.filter(user=request.user).first()
    form = UserConfigForm(instance=config)
    offers = UserOffer.objects.filter(user=request.user)[:20]

    response = render(request, 'gratka/dashboard.html', {
        'form': form,
        'config': config,
        'offers': offers,
    })

    # Mark all unread offers as read after rendering
    UserOffer.objects.filter(user=request.user, is_read=False).update(is_read=True)

    return response


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
        user_config.email = request.user.email
        user_config.save()
        return render(request, 'gratka/partials/config_success.html', {
            'config': user_config,
            'success': True,
        })

    return render(request, 'gratka/partials/config_success.html', {
        'form': form,
        'error': 'Popraw błędy w formularzu.',
    })
