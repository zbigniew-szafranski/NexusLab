from .services import SERVICES


def footer_services(request):
    """Service links for the site footer (website/base_site.html)."""
    return {'footer_services': SERVICES}
