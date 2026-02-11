class SubdomainMiddleware:
    """Routes requests to gratka.* subdomain to a dedicated URL conf."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0].lower()
        if host.startswith('gratka.'):
            request.urlconf = 'config.urls_gratka'
        return self.get_response(request)
