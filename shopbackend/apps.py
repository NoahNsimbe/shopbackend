from django.contrib.admin.apps import AdminConfig


class MyAdminConfig(AdminConfig):
    default_site = 'shopbackend.admin.MyAdminSite'
    name = 'AdminSite'
