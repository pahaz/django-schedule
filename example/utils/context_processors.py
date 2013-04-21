from django.contrib.sites.models import Site


def site(request):
    """
    Adds the site variables site_domain and site_name.

    Example usage:

        {{ site_domain }} or {{ site_name }}

    """
    current_site = Site.objects.get_current()

    return {
        'site_domain': current_site.domain,
        'site_name': current_site.name,
    }
