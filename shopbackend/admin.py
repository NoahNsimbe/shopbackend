from django.contrib import admin
from django.utils.translation import ugettext_lazy


class MyAdminSite(admin.AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('Store Site admin')

    # Text to put in each page's <h1> (and above login form).
    site_header = ugettext_lazy('Store administration')

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('Store Site administration')
