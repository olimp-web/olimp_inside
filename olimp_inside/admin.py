from django.contrib.admin import AdminSite


class CustomAdminSite(AdminSite):
    site_header = "OLIMP INSIDE"
    site_title = "OLIMP INSIDE - admin"


site = CustomAdminSite()
