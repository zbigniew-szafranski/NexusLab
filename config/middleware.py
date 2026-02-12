from django.shortcuts import redirect


class SubdomainMiddleware:
    """Routes requests to gratka.* subdomain to a dedicated URL conf."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0].lower()
        if host.startswith('gratka.'):
            request.urlconf = 'config.urls_gratka'
        return self.get_response(request)


class SubscriptionMiddleware:
    """Block access to Gratka views if the user's trial has expired
    and they don't have an active paid subscription."""

    EXEMPT_PATHS = [
        '/accounts/',
        '/admin/',
        '/cennik',
        '/subskrypcja/',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self._should_check(request):
            if not self._user_has_access(request.user):
                return redirect('subscriptions:trial_expired')
        return self.get_response(request)

    def _should_check(self, request):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return False

        host = request.get_host().split(':')[0].lower()
        is_gratka_subdomain = host.startswith('gratka.')
        is_gratka_path = request.path.startswith('/gratka/')

        if not (is_gratka_subdomain or is_gratka_path):
            return False

        for exempt in self.EXEMPT_PATHS:
            if request.path.startswith(exempt):
                return False

        return True

    def _user_has_access(self, user):
        try:
            return user.subscription.has_access
        except user.__class__.subscription.RelatedObjectDoesNotExist:
            from apps.subscriptions.models import UserSubscription
            sub = UserSubscription.objects.create(user=user)
            return sub.has_access
